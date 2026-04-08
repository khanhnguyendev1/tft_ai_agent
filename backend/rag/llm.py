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

    answer = answer.replace("**", "")
    answer = answer.replace("* ", "- ")
    answer = answer.replace("*", "")
    answer = answer.replace("---", "")

    answer = "\n".join([line.strip() for line in answer.split("\n") if line.strip()])

    return answer.strip()


def generate_answer(context, question):
    query_lower = question.lower()

    beginner_keywords = [
        "mới chơi", "new", "beginner", "làm quen",
        "chơi như nào", "hướng dẫn", "cách chơi",
        "không biết chơi", "how to play"
    ]

    is_beginner = any(k in query_lower for k in beginner_keywords)

    if is_beginner:
        prompt = f"""
    Bạn là người hướng dẫn TFT cho người mới.

    ⚠️ QUY TẮC:
    - Giải thích ĐƠN GIẢN
    - Không dùng thuật ngữ khó
    - Nếu có → phải giải thích
    - Không dùng markdown
    - Không dùng dấu ** hoặc *
    - Không dùng ---
    - Viết như chat bình thường
    ---

    Câu hỏi:
    {question}

    ---

    Trả lời:

    - TFT là gì
    - Cách chơi cơ bản
    - Người mới nên làm gì trước

    Ngắn gọn, dễ hiểu.
    """
    else:
        prompt = f"""
    Bạn là cao thủ TFT.

    CONTEXT:
    {context}

    Câu hỏi:
    {question}

    ---

    Trả lời NGẮN:

    Nếu là chiến thuật:
    - Roll hay eco
    - Có pivot không
    - Hướng build

    Nếu là đội hình:
    - Đội hình
    - Carry
    - Cách chơi
    """

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
            "top_p": 0.9
        }
    )

    answer = response.text if response.text else "Không có phản hồi"

    return clean_answer(answer)