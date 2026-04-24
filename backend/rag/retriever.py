import chromadb
from sentence_transformers import SentenceTransformer
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# ✅ giống ingest
chroma_client = chromadb.PersistentClient(path=DB_PATH)

collection = chroma_client.get_or_create_collection("tft_meta")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def build_query(state, question):
    main_trait = state.get("main_trait")

    if main_trait:
        return f"{question} TFT {main_trait}"

    return question

def retrieve(query):
    query_embedding = embedding_model.encode(query).tolist()
    query_lower = query.lower()

    keywords = ["jinx", "yasuo", "lux", "warwick", "nasus", "ahri"]

    matched = [k for k in keywords if k in query_lower]

    if matched:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            where={"type": "comp"}
        )
        return results["documents"][0]

    if "đội hình" in query_lower or "comp" in query_lower:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"type": "comp"}
        )
        return results["documents"][0]

    if "item" in query_lower or "trang bị" in query_lower:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=4
        )
        return results["documents"][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    return results["documents"][0]