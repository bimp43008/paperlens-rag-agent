from llama_index.core.llms import ChatMessage
from src.llm import get_llm

llm = get_llm()
resp = llm.chat([ChatMessage(role="user", content="Reply with exactly: OK")])
print("LLM says:", resp.message.content)