import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not API_KEY:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in .env file")


llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=API_KEY,
    base_url=BASE_URL,
)

prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a concise AI assistant. Explain {topic} in simple terms for a beginner. [/INST]"
)


parser = StrOutputParser()


def generate_explanation(topic: str) -> str:
    chain = prompt | llm | parser
    response = chain.invoke({"topic": topic})
    return response

if __name__ == "__main__":
    user_topic = input("🧠 Enter a topic to explain: ").strip()
    print("\n⏳ Generating response...\n")

    response = generate_explanation(user_topic)
    print("💬 Response:\n")
    print(response)


    os.makedirs("logs", exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": user_topic,
        "response": response,
    }

    log_file = "logs/prompt_log.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\n✅ Response logged successfully to {log_file}")
