import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize Groq LLM
llm = ChatGroq(model="llama-3.1-8b-instant")

# Define prompt template with tone
improve_prompt = PromptTemplate.from_template(
    "Rewrite the following text to make it clearer and more professional. "
    "Use a {tone} tone. Also explain briefly what was improved:\n\nText: {text}"
)

# Streamlit UI
st.set_page_config(page_title="Text Improver Tool", page_icon="📝")
st.title("📝 Text Improver Agent")

# Input text
user_text = st.text_area("Enter text to improve:", height=150)

# Tone selection
tone = st.selectbox("Choose tone for rewrite:", ["formal", "friendly", "assertive"])

# Improve button
if st.button("Improve"):
    if user_text.strip():
        prompt = improve_prompt.format(text=user_text, tone=tone)
        response = llm.invoke(prompt)
        improved_text = response.content

        # Side-by-side comparison
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📝 Original Text")
            st.write(user_text)
        with col2:
            st.subheader(f"✅ Improved Text ({tone.title()} Tone)")
            st.write(improved_text)
    else:
        st.warning("Please enter some text to improve.")