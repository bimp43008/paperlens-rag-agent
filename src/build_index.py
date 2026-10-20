from pathlib import Path

import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

DATA_DIR = Path("data/papers")
CHROMA_PATH="./chroma_db"
COLLECTION_NAME="paperlens"

def build_index():
    reader = SimpleDirectoryReader(
        input_dir=str(DATA_DIR),
    )

    documents = reader.load_data()

    db = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=20),
            embed_model,
        ],
        vector_store=vector_store,
    )

    pipeline.run(documents=documents)

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    print("Index build successfully.")
    return index

if __name__ == "__main__":
    build_index()