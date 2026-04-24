import google.generativeai as genai
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


def clean_answer(answer: str) -> str:
    for bad in ["Dựa trên", "Theo dữ liệu", "Theo thông tin", "Trong context", "Dựa vào"]:
        answer = answer.replace(bad, "")

    lines = [l.strip() for l in answer.split("\n") if l.strip()]
    return "\n".join(lines)

def agent_answer(state, context, question):
    from backend.game_logic.analyzer import analyze_board, suggest_playstyle

    analysis = analyze_board(state)

    main_trait = analysis.get("main_trait")

    # 🔥 build query thông minh
    if main_trait:
        question = f"{question} (đang chơi {main_trait})"

    answer = generate_answer(context, question)

    # 🔥 thêm gợi ý logic
    playstyle = suggest_playstyle(state)

    final_answer = f"{answer}\n\nGợi ý thêm: {playstyle}"

    return final_answer

def generate_answer(context, question, state=None):
    query_lower = question.lower()

    beginner_keywords = [
        "mới chơi", "new", "beginner", "làm quen",
        "chơi như nào", "chơi sao", "cách chơi",
        "hướng dẫn", "không biết chơi",
        "how to play", "what is tft"
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

        STATE:
        {state}

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

