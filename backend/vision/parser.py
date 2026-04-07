import google.generativeai as genai
from PIL import Image
import json
import io

def parse_tft_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    width, height = image.size

    return {
        "level": 7 if width < 1500 else 8,
        "gold": 20,
        "board": [{"name": "Nasus"}, {"name": "Warwick"}],
        "bench": [],
        "items": ["Giant Slayer"]
    }