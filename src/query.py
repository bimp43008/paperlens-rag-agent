import argparse
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.llm import get_llm


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "paperlens"


def get_query_engine():
    db = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    llm = get_llm()

    query_engine = index.as_query_engine(
        llm=llm,
        response_mode="compact",
    )

    return query_engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", type=str)
    args = parser.parse_args()

    query_engine = get_query_engine()
    response = query_engine.query(args.question)

    print("\nAnswer:")
    print(response)

    print("\nSource nodes:")
    for node in response.source_nodes:
        print(node.node_id, node.score)


if __name__ == "__main__":
    main()