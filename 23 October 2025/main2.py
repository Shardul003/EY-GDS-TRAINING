import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# Configuration
MODEL_NAME = "deepseek/deepseek-r1-0528:free"
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not API_KEY:
    st.error("❌ OPENROUTER_API_KEY not found in .env file.")
    st.stop()

# -----------------------------
# Core function to get LLM response
# -----------------------------
def get_response(user_prompt: str) -> str:
    """Send the user's prompt to the model and return the response."""
    try:
        llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=512,
            api_key=API_KEY,
            base_url=BASE_URL,
        )

        messages = [
            SystemMessage(content="You are a helpful and concise AI Study Assistant."),
            HumanMessage(content=user_prompt),
        ]

        response = llm.invoke(messages)
        return response.content.strip()

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# -----------------------------
# Streamlit User Interface
# -----------------------------
def main():
    st.set_page_config(page_title="AI Study Assistant", layout="centered")
    st.title("🧠 AI Study Assistant")
    st.markdown(f"Model in use: **`{MODEL_NAME}`** (via OpenRouter + LangChain)")
    st.divider()

    # User input section
    user_input = st.text_input(
        "Ask your study question:",
        placeholder="e.g., What are the best methods for memorizing definitions?",
        key="user_prompt",
    )

    # Output display area
    response_placeholder = st.empty()

    if st.button("Get Advice", type="primary"):
        if not user_input.strip():
            response_placeholder.error("⚠️ Please enter a question before submitting.")
            return

        with st.spinner("💭 Thinking... contacting OpenRouter..."):
            assistant_response = get_response(user_input)

        if assistant_response.startswith("❌ ERROR"):
            response_placeholder.error(assistant_response)
        else:
            response_placeholder.success("Assistant Response:")
            st.markdown(assistant_response)

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    main()
