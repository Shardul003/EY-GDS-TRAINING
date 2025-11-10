from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get API key from .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HISTORY_FILE = "qa-history.json"

# Input schema
class Prompt(BaseModel):
    query: str = Field(..., min_length=1, description="Query cannot be empty")

def load_history():
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_to_history(question, answer):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),  # Clean timestamp format
        "question": question,
        "answer": answer
    })
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

@app.get("/")
def read_root():
    return {"message": "Welcome to the OpenRouter FastAPI integration. Use POST /generate to query the model."}

@app.post("/generate")
async def generate_response(prompt: Prompt):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OpenRouter API key")

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Knowledge Assistant"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.query}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        save_to_history(prompt.query, answer)

        return {"question": prompt.query, "response": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/history")
async def get_history():
    return load_history()