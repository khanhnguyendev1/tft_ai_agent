import requests
import json
import os

SAVE_PATH = "backend/data/meta.json"

def crawl_lolchess_json():
    url = "https://lolchess.gg/__data/SET16/meta.json"  # Ví dụ URL JSON nội bộ
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("❌ Không fetch được JSON, status:", res.status_code)
        return

    data = res.json()

    # Giả sử data có comps
    comps = []
    for comp in data.get("comps", []):
        comps.append({
            "type": "comp",
            "name": comp.get("name"),
            "winRate": comp.get("winRate"),
            "pickRate": comp.get("pickRate"),
            "units": comp.get("units")
        })

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(comps, f, indent=2, ensure_ascii=False)

    print("✅ Done:", len(comps))

if __name__ == "__main__":
    crawl_lolchess_json()