from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()
app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class TaskRequest(BaseModel):
    task: str
    query: str = None
    num1: float = None
    num2: float = None
    operation: str = None

@app.post("/process")
async def process_task(data: TaskRequest):
    try:
        if data.task == "Arithmetic":
            if data.num1 is None or data.num2 is None or data.operation is None:
                raise HTTPException(status_code=400, detail="Missing numbers or operation")
            if data.operation == "Add":
                result = data.num1 + data.num2
            elif data.operation == "Subtract":
                result = data.num1 - data.num2
            elif data.operation == "Multiply":
                result = data.num1 * data.num2
            elif data.operation == "Divide":
                if data.num2 == 0:
                    raise HTTPException(status_code=400, detail="Division by zero")
                result = data.num1 / data.num2
            return {"answer": f"Result: {result}"}

        elif data.task == "Date":
            return {"answer": f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"}

        elif data.task == "Reverse":
            if not data.query:
                raise HTTPException(status_code=400, detail="Missing word to reverse")
            return {"answer": data.query[::-1]}

        elif data.task == "AI":
            if not data.query:
                raise HTTPException(status_code=400, detail="Missing query for AI")
            if not GROQ_API_KEY:
                raise HTTPException(status_code=500, detail="Missing Groq API key")

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": data.query}
                ]
            }
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            data_json = response.json()
            return {"answer": data_json["choices"][0]["message"]["content"]}

        else:
            raise HTTPException(status_code=400, detail="Invalid task")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
