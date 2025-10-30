import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize Groq LLM (Mistral)
llm = ChatGroq(model="llama-3.1-8b-instant")
# Define summarization prompt
summarization_prompt = PromptTemplate.from_template(
    "Summarize the following text clearly and concisely:\n\n{text}"
)

# Streamlit UI setup
st.set_page_config(page_title="Summarizer Tool", page_icon="📝")
st.title("📝 AI Summarizer Tool")

# Text input area
input_text = st.text_area("Enter long text or conversation to summarize:", height=200)

# Summarize button
if st.button("Summarize"):
    if input_text.strip():
        # Run the LLM with the prompt
        prompt = summarization_prompt.format(text=input_text)
        response = llm.invoke(prompt)
        st.subheader("🔍 Summary")
        st.write(response.content)
    else:
        st.warning("Please enter some text to summarize.")