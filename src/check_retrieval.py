import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

db = chromadb.PersistentClient(path="./chroma_db")
vs = ChromaVectorStore(chroma_collection=db.get_or_create_collection("paperlens"))
index = VectorStoreIndex.from_vector_store(
    vs, embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
)

retriever = index.as_retriever(similarity_top_k=3)
for n in retriever.retrieve("What are the three dimensions used to evaluate a RAG system?"):
    print(round(n.score, 3), "|", n.node.text[:100].replace("\n", " "))