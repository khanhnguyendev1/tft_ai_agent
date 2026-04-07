import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ddragon_path = os.path.join(BASE_DIR, "ddragon.json")
meta_path = os.path.join(BASE_DIR, "meta.json")
output_path = os.path.join(BASE_DIR, "tft_all_data.json")


# 📥 load ddragon
with open(ddragon_path, "r", encoding="utf-8") as f:
    ddragon = json.load(f)

# 📥 load meta (nếu có)
if os.path.exists(meta_path):
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    print("⚠️ meta.json chưa có → dùng mỗi ddragon")
    meta = []

# 🔗 merge
all_data = ddragon + meta

# 💾 save
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print(f"✅ MERGED: {len(all_data)} records")