import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.environ.get("LLM_BASE_URL", "https://api.deepseek.com"),
)

r = client.chat.completions.create(
    model=os.environ.get("LLM_MODEL", "deepseek-chat"),
    messages=[{"role": "user", "content": "Reply with exactly: OK"}],
)
print("LLM says:", r.choices[0].message.content)