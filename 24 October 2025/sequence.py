import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ======================================================
# Step 1: Environment Setup
# ======================================================
load_dotenv()

router_token = os.getenv("OPENROUTER_API_KEY")
router_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not router_token:
    raise EnvironmentError("Missing API key: 'OPENROUTER_API_KEY' not found in .env")

# ======================================================
# Step 2: Model Initialization (Mistral on OpenRouter)
# ======================================================
chat_model = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=router_token,
    base_url=router_url,
)

# ======================================================
# Step 3: Prompt Definitions
# ======================================================
explain_template = ChatPromptTemplate.from_template(
    "<s>[INST] You are an AI tutor. Provide a simple and clear explanation of {subject} for a beginner. [/INST]"
)

question_template = ChatPromptTemplate.from_template(
    "<s>[INST] From this explanation, create 3 basic quiz questions to test understanding:\n\n{explanation} [/INST]"
)

output_parser = StrOutputParser()

# ======================================================
# Step 4: Helper Functions
# ======================================================
def create_summary(subject):
    flow = explain_template | chat_model | output_parser
    return flow.invoke({"subject": subject})

def create_quiz(explanation):
    flow = question_template | chat_model | output_parser
    return flow.invoke({"explanation": explanation})

# ======================================================
# Step 5: Run the Process
# ======================================================
topic_input = input("Enter a learning topic: ").strip()
summary_text = create_summary(topic_input)
quiz_text = create_quiz(summary_text)

print("\n📘 Summary:\n", summary_text)
print("\n📝 Quiz Questions:\n", quiz_text)

# ======================================================
# Step 6: Log the Output
# ======================================================
os.makedirs("logs", exist_ok=True)

log_record = {
    "time": datetime.now().isoformat(),
    "topic": topic_input,
    "summary": summary_text,
    "quiz": quiz_text
}

log_file = "logs/learning_assistant_log.jsonl"

with open(log_file, "a", encoding="utf-8") as file:
    json.dump(log_record, file)
    file.write("\n")

print(f"\n✅ Output successfully saved in: {log_file}")
