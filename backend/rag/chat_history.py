import json
import os
from datetime import datetime
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(BASE_DIR, "chat_history.json")


def _safe_read_json(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _safe_write_json(path: str, data: List[Dict]):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    os.replace(tmp_path, path)  


def load_history() -> List[Dict]:
    return _safe_read_json(HISTORY_PATH)


def save_message(question: str, answer: str):
    history = load_history()

    history.append({
        "question": question,
        "answer": answer,
        "time": datetime.utcnow().isoformat()
    })

    _safe_write_json(HISTORY_PATH, history)