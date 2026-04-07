import chromadb
from sentence_transformers import SentenceTransformer
import json
import os

# 👉 path chuẩn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

print("DB PATH:", DB_PATH)

# ✅ dùng PersistentClient
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection("tft_meta")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text):
    return embedding_model.encode(text).tolist()


def ingest_data():
    data_path = os.path.join(os.path.dirname(__file__), "../data/patch.json")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        # Tạo text hiển thị khác nhau dựa theo type
        if item["type"] == "champion":
            ability = item.get("ability", {})
            ability_text = (
                f"Ability: {ability.get('name', '')} - {ability.get('description', '')} "
                f"(Damage: {ability.get('damage', 'N/A')}, Mana: {ability.get('manaCost', 'N/A')}, Area: {ability.get('effectArea', 'N/A')})"
            )
            traits = ", ".join(item.get("traits", []))
            text = f"{item['name']} - Tier {item['tier']} - Traits: {traits} - Cost: {item.get('cost', 'N/A')} - {ability_text}"

            metadata = {
                "type": item["type"],
                "tier": item["tier"],
                "traits": item.get("traits", []),
                "cost": item.get("cost", None)
            }

        elif item["type"] == "item":
            text = f"{item['name']} - Tier {item['tier']} - {item.get('description','')}"
            metadata = {
                "type": item["type"],
                "tier": item["tier"]
            }

        elif item["type"] == "comp":
            units = ", ".join(item.get("units", []))
            comp_items = item.get("items", {})
            comp_items_text = ", ".join(f"{k}: {v}" for k, v in comp_items.items())
            comp_traits = ", ".join(item.get("traits", []))
            text = f"{item['name']} - Tier {item['tier']} - Units: {units} - Traits: {comp_traits} - Items: {comp_items_text} - {item.get('description','')}"
            metadata = {
                "type": item["type"],
                "tier": item["tier"],
                "traits": item.get("traits", [])
            }

        elif item["type"] == "strategy":
            text = f"{item['name']} - Tier {item['tier']} - {item.get('description','')}"
            metadata = {
                "type": item["type"],
                "tier": item["tier"]
            }

        else:
            # fallback nếu type lạ
            text = f"{item.get('name', 'Unknown')} - {item.get('description','')}"
            metadata = {"type": item.get("type", "unknown")}

        print("ADDING:", text)

        collection.add(
            documents=[text],
            embeddings=[embed_text(text)],
            ids=[str(idx)],
            metadatas=[metadata]
        )

    print("✅ Data ingested successfully")


if __name__ == "__main__":
    ingest_data()