import os
from pathlib import Path 
from llama_index.llms.openai_like import OpenAILike
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)



def get_llm() -> OpenAILike:
    """
    Single source of truth for the LLM used across the project.
    Works with any OpenAI-compatible endpoint (DeepSeek, OpenRouter, vLLM, Ollama...).
    """
    return OpenAILike(
        model=os.environ.get("LLM_MODEL", "deepseek-chat"),
        api_base=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
        api_key=os.environ["LLM_API_KEY"],
        is_chat_model=True, 
        temperature=0.2,
        timeout=60.0,
    )