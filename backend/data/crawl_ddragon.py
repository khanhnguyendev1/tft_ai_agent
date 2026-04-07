import requests
import json
import os
import time

time.sleep(1)

SAVE_PATH = "backend/data/ddragon.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def get_latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        raise Exception("❌ Cannot get version")

    return res.json()[0]


def fetch_ddragon():
    version = get_latest_version()

    base = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US"

    urls = {
        "champions": f"{base}/tft-champion.json",
        "traits": f"{base}/tft-trait.json",
        "items": f"{base}/tft-item.json"
    }

    all_data = []

    for key, url in urls.items():

        print(f"👉 Fetching {key}: {url}")

        # 🔥 FIX Ở ĐÂY
        res = requests.get(url, headers=HEADERS)

        print("STATUS:", res.status_code)

        if res.status_code != 200:
            print("❌ FAIL:", res.text[:200])
            continue

        data = res.json()

        for obj_id, obj in data["data"].items():

            # 🔥 1. CHỈ LẤY SET 16
            if not obj_id.startswith("TFT16"):
                continue

            name = obj.get("name", "")

            # 🔥 2. LOẠI DATA RÁC
            if not name:
                continue

            if "@" in name:
                continue

            if "DEBUG" in obj_id:
                continue

            if "Test" in obj_id:
                continue

            # 🔥 3. CHUẨN HÓA DATA
            if key == "champions":
                all_data.append({
                    "type": "champion",
                    "name": name,
                    "cost": obj.get("cost"),
                    "traits": obj.get("traits", []),
                    "ability": obj.get("ability", {}).get("desc", "")
                })

            elif key == "items":
                all_data.append({
                    "type": "item",
                    "name": name
                })

            elif key == "traits":
                all_data.append({
                    "type": "trait",
                    "name": name
                })

    # 🔥 THÊM ĐOẠN NÀY
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_data)} records to ddragon.json")

    return all_data

if __name__ == "__main__":
    fetch_ddragon()