import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "openai/gpt-oss-120b:fastest")

client = InferenceClient(
    model=HF_MODEL_ID,          # specify the model here
    api_key=HF_API_TOKEN,
)

def call_hf_llm(prompt: str, max_new_tokens: int = 256) -> str:
    completion = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_new_tokens,
    )

    text = ""
    for choice in completion.choices:
        msg = getattr(choice, "message", None)
        if msg and msg.get("content"):
            text += msg["content"]
        delta = getattr(choice, "delta", None)
        if delta and getattr(delta, "content", None):
            text += delta.content
    return text
