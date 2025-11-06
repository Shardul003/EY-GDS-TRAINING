import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage

# ------------------------------------------------------------
# 1. Environment Setup
# ------------------------------------------------------------
load_dotenv()
router_key = os.getenv("OPENROUTER_API_KEY")
router_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not router_key:
    raise ValueError("Missing OPENROUTER_API_KEY in environment")

# ------------------------------------------------------------
# 2. Language Model Initialization
# ------------------------------------------------------------
chat_engine = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=router_key,
    base_url=router_url,
)

# ------------------------------------------------------------
# 3. Utility Functions
# ------------------------------------------------------------
def word_count(text: str) -> int:
    return len(text.split())

def reverse_words(text: str) -> str:
    return " ".join(text.split()[::-1])

def define_term(term: str) -> str:
    prompt = ChatPromptTemplate.from_template(
        f"<s>[INST] You are a concise assistant. Define the word '{term}' in 1–2 sentences.[/INST]"
    )
    formatted = prompt.format()
    response = chat_engine.invoke(formatted)
    return response.content.strip()

# ------------------------------------------------------------
# 4. Memory Setup
# ------------------------------------------------------------
chat_history = ConversationBufferMemory(memory_key="chat_log", return_messages=True)

# ------------------------------------------------------------
# 5. Interactive Chat Loop
# ------------------------------------------------------------
print("\n=== Welcome to the Interactive Chat Agent ===")
print("Type 'exit' to leave the session.\n")

while True:
    user_text = input("You: ").strip()
    if user_text.lower() == "exit":
        print("\nSession closed. Goodbye!")
        break

    # Word count command
    if user_text.lower().startswith("count"):
        try:
            phrase = " ".join(user_text.split()[1:])
            total = word_count(phrase)
            reply = f"Agent: That sentence contains {total} words."
            print(reply)
            chat_history.save_context({"input": user_text}, {"output": reply})
            continue
        except Exception as err:
            print(f"Agent: Error occurred: {err}")
            continue

    # Reverse command
    if user_text.lower().startswith("reverse"):
        try:
            phrase = " ".join(user_text.split()[1:])
            reversed_text = reverse_words(phrase)
            print(f"Agent: {reversed_text}")
            chat_history.save_context({"input": user_text}, {"output": reversed_text})
            continue
        except Exception as err:
            print(f"Agent: Error occurred: {err}")
            continue

    # Define command
    if user_text.lower().startswith("define"):
        try:
            term = " ".join(user_text.split()[1:])
            definition = define_term(term)
            print(f"Agent: {definition}")
            chat_history.save_context({"input": user_text}, {"output": definition})
            continue
        except Exception as err:
            print(f"Agent: Error occurred: {err}")
            continue

    # General LLM response
    try:
        result = chat_engine.invoke(user_text)
        print("Agent:", result.content)
        chat_history.save_context({"input": user_text}, {"output": result.content})
    except Exception as err:
        print("Agent: Unexpected error:", err)
