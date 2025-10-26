import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# ==============================================================
# Step 1: Environment Setup
# ==============================================================

load_dotenv()

router_key = os.getenv("OPENROUTER_API_KEY")
router_endpoint = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not router_key:
    raise EnvironmentError("Missing API key: Please set OPENROUTER_API_KEY in .env file")

# ==============================================================
# Step 2: Model Configuration
# ==============================================================

chatbot = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=router_key,
    base_url=router_endpoint,
)

# ==============================================================
# Step 3: Generate AI Response
# ==============================================================

conversation = [
    SystemMessage(content="You are an informative and concise assistant."),
    HumanMessage(content="<s>[INST] Describe reinforcement learning in easy words. [/INST]"),
]

ai_reply = chatbot.invoke(conversation)
reply_text = ai_reply.content.strip()

print("AI Response:", reply_text)

# ==============================================================
# Step 4: Save Logs
# ==============================================================

interaction_log = {
    "timestamp": datetime.utcnow().isoformat(),
    "model_name": "mistralai/mistral-7b-instruct",
    "query": conversation[-1].content,
    "answer": reply_text,
    "user_feedback": None,
}

os.makedirs("logs", exist_ok=True)
log_path = "logs/ai_interaction_log.jsonl"

with open(log_path, "a", encoding="utf-8") as log_file:
    json.dump(interaction_log, log_file)
    log_file.write("\n")

print(f"Interaction details saved at: {log_path}")

# ==============================================================
# Step 5: Collect Feedback
# ==============================================================

user_ratin_
