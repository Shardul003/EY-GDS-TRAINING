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

# Define sentiment analysis prompt
sentiment_prompt = PromptTemplate.from_template(
    "Analyze the sentiment of the following text and classify it as Positive, Neutral, or Negative. "
    "Also explain briefly why:\n\nText: {text}"
)

# Streamlit UI
st.set_page_config(page_title="Sentiment Analyzer", page_icon="🧠")
st.title("🧠 Sentiment Analyzer Tool")

# Input text
user_text = st.text_area("Enter text to analyze sentiment:", height=150)

# Emoji mapping
emoji_map = {
    "positive": "😊",
    "neutral": "😐",
    "negative": "😞"
}

# Analyze button
if st.button("Analyze"):
    if user_text.strip():
        prompt = sentiment_prompt.format(text=user_text)
        response = llm.invoke(prompt)
        result_text = response.content

        # Detect sentiment keyword and attach emoji
        sentiment = "neutral"  # default
        for key in emoji_map:
            if key in result_text.lower():
                sentiment = key
                break

        st.subheader(f"{emoji_map[sentiment]} Sentiment Analysis Result")
        st.write(result_text)
    else:
        st.warning("Please enter some text to analyze.")