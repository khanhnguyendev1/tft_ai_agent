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


def retrieve(query):
    query_embedding = embedding_model.encode(query).tolist()
    query_lower = query.lower()

    # 🎯 detect intent
    if any(x in query_lower for x in ["đội hình", "comp"]):
        filter_type = "comp"
        n = 5

    elif any(x in query_lower for x in ["item", "trang bị", "build"]):
        filter_type = "item"
        n = 4

    else:
        filter_type = "comp"
        n = 5

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n,
        where={"type": filter_type}
    )

    docs = results.get("documents", [[]])[0]

    # 🔥 format lại cho Gemini
    formatted_docs = []
    for i, doc in enumerate(docs):
        formatted_docs.append(f"[DATA {i+1}] {doc}")

    return formatted_docs