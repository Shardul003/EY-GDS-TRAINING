import streamlit as st
import re
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize Groq LLM
llm = ChatGroq(model="mixtral-8x7b-32768")
# Define LangChain prompt template
priority_prompt = PromptTemplate.from_template(
    "You are a smart assistant that classifies tasks into HIGH, MEDIUM, or LOW priority.\n"
    "Task: {task}\n"
    "Respond with only one word: HIGH, MEDIUM, or LOW."
)

# Rule-based classifier
class TaskPriorityAgent:
    def __init__(self):
        self.high_priority_keywords = {
            "urgent", "asap", "tonight", "deadline", "submit", "report",
            "meeting", "presentation", "immediately", "today", "important"
        }
        self.medium_priority_keywords = {
            "schedule", "follow-up", "reminder", "prepare", "review",
            "plan", "check", "update", "respond"
        }
        self.low_priority_keywords = {
            "buy", "clean", "organize", "decorate", "snacks", "casual",
            "optional", "later", "someday", "browse"
        }

    def classify_task(self, task: str) -> str:
        task_clean = task.lower()

        if self.contains_keywords(task_clean, self.high_priority_keywords):
            priority = "HIGH"
        elif self.contains_keywords(task_clean, self.medium_priority_keywords):
            priority = "MEDIUM"
        elif self.contains_keywords(task_clean, self.low_priority_keywords):
            priority = "LOW"
        else:
            priority = self.llm_infer_priority(task)

        return f'Agent: Task “{task}” marked as {priority} priority.'

    def contains_keywords(self, text: str, keywords: set) -> bool:
        return any(re.search(rf'\b{kw}\b', text) for kw in keywords)

    def llm_infer_priority(self, task: str) -> str:
        prompt = priority_prompt.format(task=task)
        response = llm.invoke(prompt)
        return response.content.strip().upper()

# Streamlit UI
st.set_page_config(page_title="Task Priority Classifier", page_icon="⚡")
st.title("⚡ Task Priority Classifier Agent")
st.write("Enter a task description to classify its priority level.")

task_input = st.text_input("Task Description", placeholder="e.g. Submit proposal by tonight")

if st.button("Classify"):
    if task_input.strip():
        agent = TaskPriorityAgent()
        result = agent.classify_task(task_input)
        st.success(result)
    else:
        st.warning("Please enter a task description.")