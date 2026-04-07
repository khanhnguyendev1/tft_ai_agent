import google.generativeai as genai
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

print("ENV PATH:", ENV_PATH)

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("GOOGLE_API_KEY")

print("DEBUG API KEY:", api_key)

genai.configure(api_key="***")

model = genai.GenerativeModel("gemini-2.5-flash")


def clean_answer(answer):
    bad_patterns = [
        "Dựa trên",
        "Theo dữ liệu",
        "Theo thông tin",
        "Trong context",
        "Dựa vào"
    ]

    for bad in bad_patterns:
        answer = answer.replace(bad, "")

    answer = "\n".join([line.strip() for line in answer.split("\n") if line.strip()])

    return answer.strip()


def generate_answer(context, question):
    try:
        prompt = f"""
        Bạn là cao thủ TFT rank Challenger.

        ⚠️ BẮT BUỘC:
        - Trả lời NGẮN (2-4 dòng)
        - Phải đưa ra quyết định rõ ràng
        - Không nói chung chung

        ---

        CONTEXT:
        {context}

        ---

        QUESTION:
        {question}

        ---

        FORMAT:

        Nếu COMP:
        - Đội hình:
        - Carry:
        - Cách chơi:

        Nếu GAME STATE:
        - Roll hay Eco
        - Giữ hay pivot
        - Hướng build

        ---

        Trả lời:
        """

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.6,
                "top_p": 0.9
            }
        )

        answer = getattr(response, "text", None)

        if not answer:
            return "AI không phản hồi"

        return clean_answer(answer)

    except Exception as e:
        return f"Lỗi Gemini: {str(e)}"