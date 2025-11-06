import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain

# Load environment variables
load_dotenv()

# ------------------------------------------------------------------
# Retrieve API credentials
router_api_key = os.getenv("OPENROUTER_API_KEY")
router_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not router_api_key:
    raise ValueError("Missing OPENROUTER_API_KEY in .env file")

# Initialize the language model
chat_model = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=router_api_key,
    base_url=router_base_url,
)

# Setup memory and conversation chain
chat_memory = ConversationBufferMemory(return_messages=True)
chat_chain = ConversationChain(llm=chat_model, memory=chat_memory)

# Start interactive session
print("\n=== Chat with the AI Agent ===")
print("Type 'exit' to end the conversation.\n")

while True:
    user_message = input("You: ").strip()
    if user_message.lower() == "exit":
        print("\nConversation ended. Have a great day!")
        break
    try:
        response = chat_chain(user_message)
        print("Agent:", response['response'])
    except Exception as err:
        print("Agent: Sorry, something went wrong.")
        print("Error:", err)
