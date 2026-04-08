import google.generativeai as genai
from PIL import Image
import io
import json
import os

genai.configure(api_key="***")

model = genai.GenerativeModel("gemini-2.5-flash")

def parse_tft_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    prompt = """
Bạn là AI phân tích TFT.

Từ ảnh game TFT, hãy trích xuất:

- level (int)
- gold (int, ước lượng nếu không thấy)
- board (list tướng trên bàn)
- bench (list tướng dự bị nếu thấy)
- items (list item thấy được)

Trả về JSON format:

{
  "level": 8,
  "gold": 20,
  "board": [{"name": "Jinx"}, {"name": "Ekko"}],
  "bench": [],
  "items": ["Giant Slayer", "Guinsoo"]
}

⚠️ QUAN TRỌNG:
- Chỉ trả JSON
- Không giải thích
"""

    response = model.generate_content([
        prompt,
        image
    ])

    text = response.text.strip()

    # 🔥 clean markdown nếu có
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]

    try:
        data = json.loads(text)
        return data
    except:
        print("PARSE ERROR:", text)
        return None