# app.py

import os
from io import BytesIO
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# LangChain / models
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.prompts import PromptTemplate

# PDF extraction
from pypdf import PdfReader

# -------------------------------
# ENV / CONFIG
# -------------------------------
load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

DEFAULT_INDEX_DIR = str(Path.cwd() / "my_vectorstore123")

st.set_page_config(page_title="Budget Chatbot", page_icon="💬")

# -------------------------------
# CACHED RESOURCES
# -------------------------------

@st.cache_resource(show_spinner=False)
def get_embeddings():
    # Uses sentence-transformers/all-MiniLM-L6-v2
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@st.cache_resource(show_spinner=False)
def get_llm():
    # Fast chat model; ensure GROQ_API_KEY is set
    return ChatGroq(model="llama-3.1-8b-instant")

# -------------------------------
# HELPERS
# -------------------------------

def extract_text_from_pdf_file(uploaded_file) -> list[Document]:
    """
    Extract text from a Streamlit UploadedFile using pypdf.
    Returns a list of Documents (one per page) with metadata.
    """
    name = uploaded_file.name
    file_bytes = uploaded_file.read()
    reader = PdfReader(BytesIO(file_bytes))
    docs = []
    for i, page in enumerate(reader.pages):
        txt = page.extract_text() or ""
        if txt.strip():
            docs.append(
                Document(
                    page_content=txt,
                    metadata={"source": name, "page": i + 1}
                )
            )
    return docs

def extract_text_from_txt_file(uploaded_file) -> list[Document]:
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    return [Document(page_content=content, metadata={"source": uploaded_file.name})]

def chunk_documents(documents, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)

def build_faiss_from_docs(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)

def save_index(vectorstore, index_dir):
    Path(index_dir).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(index_dir)

def load_index(index_dir, embeddings):
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

def format_chat_history_for_prompt(history):
    """
    Convert st.session_state["messages"] -> readable string.
    """
    lines = []
    for m in history:
        role = m["role"].capitalize()
        lines.append(f"{role}: {m['content']}")
    return "\n".join(lines)

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! Upload PDFs and ask me anything about the budget documents."}
    ]
if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None
if "last_index_dir" not in st.session_state:
    st.session_state["last_index_dir"] = DEFAULT_INDEX_DIR
if "loaded_sources" not in st.session_state:
    st.session_state["loaded_sources"] = set()

# -------------------------------
# SIDEBAR (Index Management)
# -------------------------------
with st.sidebar:
    st.header("📚 Knowledge Base")
    index_dir = st.text_input("Index directory", value=st.session_state["last_index_dir"])
    st.session_state["last_index_dir"] = index_dir

    # Upload controls
    uploaded_files = st.file_uploader(
        "Upload PDF/TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    build_mode = st.radio(
        "Build mode",
        options=["Replace index", "Append to current"],
        help="Replace will discard the current vectorstore; Append adds new chunks."
    )
    chunk_size = st.number_input("Chunk size", min_value=200, max_value=3000, value=1000, step=100)
    chunk_overlap = st.number_input("Chunk overlap", min_value=0, max_value=500, value=100, step=10)
    persist = st.checkbox("Persist index to disk after build", value=True)

    colA, colB, colC = st.columns(3)
    with colA:
        build_btn = st.button("Build/Update Index", use_container_width=True)
    with colB:
        load_btn = st.button("Load Existing Index", use_container_width=True)
    with colC:
        clear_btn = st.button("Clear Index", use_container_width=True)

    st.divider()
    k = st.slider("Top‑K documents to retrieve", 1, 10, 3)
    st.caption("Tip: Larger K can improve recall but may slow responses.")

# -------------------------------
# BUILD / LOAD / CLEAR INDEX ACTIONS
# -------------------------------
embeddings = get_embeddings()

if build_btn:
    if not uploaded_files:
        st.warning("Please upload at least one PDF/TXT file.")
    else:
        with st.spinner("Building index from uploaded files..."):
            all_docs = []
            for f in uploaded_files:
                if f.name.lower().endswith(".pdf"):
                    all_docs.extend(extract_text_from_pdf_file(f))
                else:
                    all_docs.extend(extract_text_from_txt_file(f))

            if not all_docs:
                st.error("No extractable text found in the uploaded files.")
            else:
                chunks = chunk_documents(all_docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

                if build_mode == "Replace index" or st.session_state["vectorstore"] is None:
                    vs = build_faiss_from_docs(chunks, embeddings)
                else:
                    # Append to existing index
                    vs = st.session_state["vectorstore"]
                    vs.add_documents(chunks)

                st.session_state["vectorstore"] = vs
                for d in all_docs:
                    st.session_state["loaded_sources"].add(d.metadata.get("source", "unknown"))

                if persist:
                    save_index(st.session_state["vectorstore"], index_dir)
                    st.success(f"Index saved to: {index_dir}")
                else:
                    st.info("Index updated in memory (not persisted).")

if load_btn:
    try:
        with st.spinner(f"Loading index from {index_dir}..."):
            st.session_state["vectorstore"] = load_index(index_dir, embeddings)
            st.success(f"Loaded index from: {index_dir}")
    except Exception as e:
        st.error(f"Failed to load index: {e}")

if clear_btn:
    st.session_state["vectorstore"] = None
    st.session_state["loaded_sources"] = set()
    st.success("Cleared in-memory index. (Files on disk are unchanged)")

# -------------------------------
# MAIN APP
# -------------------------------
st.title("💬 Budget Chatbot Assistant")

# Show loaded sources
if st.session_state["loaded_sources"]:
    st.caption("Loaded sources: " + " | ".join(sorted(st.session_state["loaded_sources"])))
elif st.session_state["vectorstore"] is not None:
    st.caption("Vectorstore loaded, but sources not tracked for this session.")
else:
    st.caption("No index loaded yet. Upload PDFs or load an existing index.")

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Guardrail if no index
if st.session_state["vectorstore"] is None:
    st.info("⬆️ Upload and build an index (or load an existing one) to start chatting.")
    # Still allow user to type; we'll just inform them
    user_input = st.chat_input("Ask a question...")
    if user_input:
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write("Please build or load an index first.")
    st.stop()

# -------------------------------
# RAG CHAIN (history-aware)
# -------------------------------
llm = get_llm()
retriever = st.session_state["vectorstore"].as_retriever(search_kwargs={"k": k})

context_prompt = PromptTemplate.from_template(
    "Refactor the question using chat history for context.\n\n"
    "Chat History:\n{chat_history}\n\n"
    "Question:\n{input}"
)

history_aware_ret = create_history_aware_retriever(llm, retriever, context_prompt)

qa_prompt = PromptTemplate.from_template(
    "You are a budget assistant. Only use the provided context to answer the question. "
    "If the answer is not in the context, say 'I don't know.' Do not use prior knowledge.\n\n"
    "Context:\n{context}\n\n"
    "Chat History:\n{chat_history}\n\n"
    "Question:\n{input}"
)

from langchain.chains.combine_documents import create_stuff_documents_chain
qa_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_ret, qa_chain)

# -------------------------------
# CHAT INPUT LOOP
# -------------------------------
if user_input := st.chat_input("Ask a question..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        chat_history_str = format_chat_history_for_prompt(st.session_state["messages"])
        try:
            result = rag_chain.invoke({"input": user_input, "chat_history": chat_history_str})
            answer = result.get("answer", "I don't know.")
        except Exception as e:
            answer = f"Error while generating answer: {e}"

        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.write(answer)

# Utility buttons
c1, c2 = st.columns(2)
with c1:
    if st.button("♻️ Reset Chat"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Chat reset. Ask me anything about the loaded documents."}
        ]
        st.experimental_rerun()
with c2:
    if st.button("🧹 Clear In‑Memory Index"):
        st.session_state["vectorstore"] = None
        st.session_state["loaded_sources"] = set()
        st.experimental_rerun()
