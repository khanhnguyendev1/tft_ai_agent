import google.generativeai as genai
from PIL import Image
import io
import json
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, "backend/.env")

load_dotenv(ENV_PATH)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash") 

def fallback_game_state():
    return {
        "level": 7,
        "gold": 0,
        "board": [],
        "bench": [],
        "items": []
    }


def parse_tft_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        image.thumbnail((1024, 1024))

        prompt = """
Bạn là AI phân tích TFT.

BẮT BUỘC:
- Chỉ trả về JSON hợp lệ
- Không markdown
- Không text ngoài JSON

Schema:
{
  "level": number,
  "gold": number,
  "board": [{"name": "string"}],
  "bench": [{"name": "string"}],
  "items": ["string"]
}

Nếu không chắc → dùng default:
level=7, gold=0, list=[]
"""

        response = model.generate_content(
            [prompt, image],
            generation_config={
                "temperature": 0.2
            }
        )

        # 🔥 lấy text an toàn
        text = None

        if hasattr(response, "text") and response.text:
            text = response.text
        else:
            try:
                text = response.candidates[0].content.parts[0].text
            except Exception as e:
                print("❌ NO TEXT:", e)
                return fallback_game_state()

        text = text.strip()
        print("📥 RAW GEMINI:", text)

        # 🔥 remove markdown nếu có
        if "```" in text:
            parts = text.split("```")
            text = parts[1] if len(parts) > 1 else text
            if text.startswith("json"):
                text = text[4:]

        text = text.strip()

        # 🔥 extract JSON chuẩn
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == -1:
            print("❌ NO JSON FOUND")
            return fallback_game_state()

        json_str = text[start:end]

        try:
            data = json.loads(json_str)
        except Exception as e:
            print("❌ JSON PARSE FAIL:", e)
            return fallback_game_state()

        # 🔥 đảm bảo đủ field
        data["level"] = int(data.get("level", 7) or 7)
        data["gold"] = int(data.get("gold", 0) or 0)
        data["board"] = data.get("board") or []
        data["bench"] = data.get("bench") or []
        data["items"] = data.get("items") or []

        return data

    except Exception as e:
        print("🔥 PARSE ERROR:", str(e))
        return fallback_game_state()