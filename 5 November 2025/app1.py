import os
import tempfile
from pathlib import Path
from typing import List

import streamlit as st
from dotenv import load_dotenv

# Loaders / splitters / docs
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Vector store & embeddings & model
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Prompts
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ✅ Classic chains & retrievers (v1+ live here)
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.retrievers import MultiQueryRetriever


# ────────────────────────────────────────────────────────────────────────────────
# Environment
# ────────────────────────────────────────────────────────────────────────────────
load_dotenv()
# Set for downstream libs; safe if empty
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")


# ────────────────────────────────────────────────────────────────────────────────
# Config / UI
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="RAG PDF Chatbot", page_icon="📄", layout="wide")
st.title("📄 RAG Chatbot with PDF Upload")

DEFAULT_INDEX_DIR = os.path.abspath("./storage/faiss_index")
Path(DEFAULT_INDEX_DIR).mkdir(parents=True, exist_ok=True)


# ────────────────────────────────────────────────────────────────────────────────
# Helpers: uploads → Documents → chunks → FAISS
# ────────────────────────────────────────────────────────────────────────────────
def _tempfile_from_upload(upload_file, suffix: str) -> str:
    """Write a Streamlit UploadedFile to a real temp file and return the path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload_file.read())
        return tmp.name


def load_docs_from_uploads(uploaded_files: List[st.runtime.uploaded_file_manager.UploadedFile]) -> List[Document]:
    """
    Accepts a list of st.file_uploader files. Supports .pdf and .txt.
    Returns: list[Document] with metadata['source'] and (for PDFs) metadata['page'].
    """
    docs: List[Document] = []
    for uf in uploaded_files:
        name_lower = uf.name.lower()
        if name_lower.endswith(".pdf"):
            tmp_pdf = _tempfile_from_upload(uf, ".pdf")
            loader = PyPDFLoader(tmp_pdf)  # Each page becomes a Document with metadata['page'] (0-based)
            page_docs = loader.load()
            # Add a human-friendly source name for citations
            for d in page_docs:
                d.metadata["source"] = uf.name  # preserve original file name
            docs.extend(page_docs)

        elif name_lower.endswith(".txt"):
            tmp_txt = _tempfile_from_upload(uf, ".txt")
            loader = TextLoader(tmp_txt, encoding="utf-8")
            text_docs = loader.load()
            for d in text_docs:
                d.metadata["source"] = uf.name  # no page for TXT by default
            docs.extend(text_docs)

        else:
            st.warning(f"Unsupported file type: {uf.name}. Only .pdf and .txt are allowed.")
    return docs


def chunk_documents(documents: List[Document], chunk_size=1000, chunk_overlap=100) -> List[Document]:
    """
    Split documents into chunks while preserving metadata (source, page).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        add_start_index=True,  # helpful if you want to show local offsets later
    )
    chunks = splitter.split_documents(documents)
    # Add a stable chunk id for traceability (optional)
    for i, d in enumerate(chunks, start=1):
        d.metadata.setdefault("chunk_id", i)
    return chunks


def build_embeddings():
    # Same sentence transformer as your earlier code
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_or_update_faiss(docs: List[Document], embeddings, existing_vs: FAISS | None = None) -> FAISS | None:
    """
    If existing_vs is provided, append docs into it; else create a new FAISS.
    """
    if not docs:
        return existing_vs
    if existing_vs is None:
        return FAISS.from_documents(docs, embeddings)
    existing_vs.add_documents(docs)
    return existing_vs


def persist_index(vectorstore: FAISS, path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(path)


def load_index(path: str, embeddings) -> FAISS | None:
    if not Path(path).exists():
        return None
    try:
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)  # trusted path
    except Exception:
        return None


# ────────────────────────────────────────────────────────────────────────────────
# LLM + RAG Chains
# ────────────────────────────────────────────────────────────────────────────────
def build_llm(model_name: str = "llama-3.1-8b-instant") -> ChatGroq:
    """
    Initialize Groq chat model. Requires GROQ_API_KEY in env.
    """
    return ChatGroq(model=model_name)


def build_chains(vectorstore: FAISS, llm: ChatGroq):
    """
    Build MultiQuery → HistoryAware retriever → QA chain → Retrieval chain.
    Returns (rag_chain, history_aware_retriever) so we can use the retriever for citation fallback.
    """
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    # MultiQuery retriever (diversify queries to improve recall)
    try:
        multiquery_retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)
    except Exception:
        multiquery_retriever = base_retriever

    # Prompt to rewrite follow-up questions into standalone ones
    rephrase_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given the chat history and the latest user question, "
                "reformulate a standalone query that can be understood without the history. "
                "Do NOT answer; return only the rewritten query."
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_ret = create_history_aware_retriever(
        llm=llm,
        retriever=multiquery_retriever,
        prompt=rephrase_prompt,
    )

    # System prompt for final answer
    system_prompt = (
        "You are a helpful assistant. Use the retrieved context to answer the question.\n"
        "If unsure, say: \"I don't know.\""
        "\nContext:\n{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_ret, qa_chain)
    return rag_chain, history_aware_ret


# ────────────────────────────────────────────────────────────────────────────────
# Sidebar: Upload, (Re)build index, Model
# ────────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    model_name = st.selectbox(
        "Groq model",
        options=[
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
        ],
        index=0,
    )
    index_dir = st.text_input("Index folder", value=DEFAULT_INDEX_DIR)
    uploaded = st.file_uploader(
        "Upload PDFs/TXTs to index",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files and then click 'Build/Update Index'.",
    )

    col_a, col_b = st.columns(2)
    build_clicked = col_a.button("📦 Build/Update Index", use_container_width=True)
    clear_index = col_b.button("🗑️ Clear Index", type="secondary", use_container_width=True)

    if clear_index:
        try:
            for p in Path(index_dir).glob("*"):
                if p.is_file():
                    p.unlink()
                else:
                    # remove any nested files (safety)
                    for q in p.rglob("*"):
                        if q.is_file():
                            q.unlink()
                    p.rmdir()
            st.success("Index folder cleared.")
        except Exception as e:
            st.error(f"Failed to clear index: {e}")

# Build / update index on demand
if build_clicked:
    if not uploaded:
        st.warning("Please upload at least one PDF or TXT.")
    else:
        with st.spinner("Building / updating index..."):
            emb = build_embeddings()
            existing_vs = load_index(index_dir, emb)
            raw_docs = load_docs_from_uploads(uploaded)
            chunks = chunk_documents(raw_docs, chunk_size=1000, chunk_overlap=100)
            vs = create_or_update_faiss(chunks, emb, existing_vs)
            if vs is None:
                st.error("Failed to build index: no documents.")
            else:
                persist_index(vs, index_dir)
                st.success(f"Index ready at: {index_dir} (chunks: {len(chunks)})")


# ────────────────────────────────────────────────────────────────────────────────
# Chat area
# ────────────────────────────────────────────────────────────────────────────────
# Load vector store (if exists)
embeddings = build_embeddings()
vectorstore = load_index(index_dir, embeddings)

if vectorstore is None:
    st.info("No index found. Upload PDFs/TXTs in the sidebar and click **Build/Update Index**.")
else:
    llm = build_llm(model_name)
    rag_chain, history_ret = build_chains(vectorstore, llm)

    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi! Upload PDFs in the sidebar, then ask a question."}
        ]

    # Display chat history
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about your documents...")
    if user_input:
        # Append user turn
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # Compute chat_history for chains
        chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]]

        with st.chat_message("assistant"):
            try:
                # Run RAG
                result = rag_chain.invoke({"input": user_input, "chat_history": chat_history})

                # Extract answer
                answer = result.get("answer", "I don't know.")
                st.session_state["messages"].append({"role": "assistant", "content": answer})
                st.write(answer)

                # ------- Citations with PDF page numbers (or chunk fallback) -------
                try:
                    docs = result.get("context", None)
                    if not isinstance(docs, list):
                        # Some chain versions may not attach docs in result; call retriever directly
                        docs = history_ret.invoke({"input": user_input, "chat_history": chat_history})

                    if docs:
                        st.markdown("**Sources:**")
                        shown = set()
                        for d in docs:
                            src = d.metadata.get("source", "Unknown source")
                            page = d.metadata.get("page", None)        # For PDFs (often 0-based)
                            chunk_id = d.metadata.get("chunk_id", None)
                            name = Path(src).name if src else "Unknown source"

                            # Convert to 1-based page numbers for PDFs
                            display_page = page
                            if isinstance(page, int) and name.lower().endswith(".pdf"):
                                display_page = page + 1

                            key = (name, display_page if display_page is not None else chunk_id)
                            if key in shown:
                                continue
                            shown.add(key)

                            if display_page is not None:
                                st.markdown(f"- {name}, **page {display_page}**")
                            elif chunk_id is not None:
                                st.markdown(f"- {name}, **chunk {chunk_id}**")
                            else:
                                st.markdown(f"- {name}")

                            if len(shown) >= 5:  # show up to 5 unique citations
                                break
                except Exception:
                    # Don't block the answer if citations fail to render
                    pass
                # -------------------------------------------------------------------

            except Exception as e:
                error_msg = f"Error during response generation: {e}"
                st.session_state["messages"].append({"role": "assistant", "content": error_msg})
                st.write(error_msg)