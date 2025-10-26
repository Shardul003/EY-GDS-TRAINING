import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
from sentence_transformers import SentenceTransformer, util

# =====================================
# 1. Load environment variables
# =====================================
load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not OPENROUTER_KEY:
    raise EnvironmentError("❌ Missing OPENROUTER_API_KEY in .env file")

# =====================================
# 2. Initialize language models
# =====================================
mistral_7b = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=OPENROUTER_KEY,
    base_url=OPENROUTER_URL,
)

mixtral_8x7b = ChatOpenAI(
    model="mistralai/mixtral-8x7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=OPENROUTER_KEY,
    base_url=OPENROUTER_URL,
)

# =====================================
# 3. Define system + user prompts
# =====================================
chat_sequence = [
    SystemMessage(content="You are a clear and helpful AI explainer."),
    HumanMessage(content="<s>[INST] Explain reinforcement learning in simple terms. [/INST]"),
]

# =====================================
# 4. Generate model responses
# =====================================
output_mistral = mistral_7b.invoke(chat_sequence).content.strip()
output_mixtral = mixtral_8x7b.invoke(chat_sequence).content.strip()

print("\n--- Output: Mistral 7B ---")
print(output_mistral)
print("\n--- Output: Mixtral 8x7B ---")
print(output_mixtral)

# =====================================
# 5. Compare and evaluate responses
# =====================================
# BLEU score
smoother = SmoothingFunction().method1
bleu_val = sentence_bleu([output_mistral.split()], output_mixtral.split(), smoothing_function=smoother)

# ROUGE score
rouge_evaluator = Rouge()
rouge_result = rouge_evaluator.get_scores(output_mistral, output_mixtral)[0]

# Cosine similarity (semantic similarity)
model_embedder = SentenceTransformer("all-MiniLM-L6-v2")
embedding_a = model_embedder.encode(output_mistral, convert_to_tensor=True)
embedding_b = model_embedder.encode(output_mixtral, convert_to_tensor=True)
similarity_score = float(util.cos_sim(embedding_a, embedding_b))

# =====================================
# 6. Display evaluation metrics
# =====================================
print("\n--- Comparison Metrics ---")
print(f"BLEU Score :  {bleu_val:.4f}")
print(f"ROUGE-1 F1 :  {rouge_result['rouge-1']['f']:.4f}")
print(f"ROUGE-L F1 :  {rouge_result['rouge-l']['f']:.4f}")
print(f"Cosine Sim :  {similarity_score:.4f}")
