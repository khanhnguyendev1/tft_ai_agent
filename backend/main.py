from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from backend.rag.retriever import retrieve
from backend.rag.llm import generate_answer
from backend.vision.parser import parse_tft_image
from backend.vision.postprocess import clean_game_state
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Form
import os
import uuid

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
def serve_ui():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        docs = retrieve(request.question) or []

        # 🔥 giới hạn context (tránh Gemini bị loãng)
        context = "\n".join(docs[:4])

        answer = generate_answer(context, request.question)
        save_message(request.question, answer)
        return {
            "context_used": docs,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form("")
):
    try:
        contents = await file.read()

        game_state = parse_tft_image(contents)
        game_state = clean_game_state(game_state)

        # 🔥 build prompt đúng
        base_prompt = f"""
Game state:

Level: {game_state.get('level')}
Gold: {game_state.get('gold')}
Board: {[c.get('name') for c in game_state.get('board', [])]}
Items: {game_state.get('items')}
"""

        if question:
            final_question = base_prompt + "\n\nUser hỏi: " + question
        else:
            final_question = base_prompt + "\n\nNên làm gì tiếp?"

        docs = retrieve(final_question)
        context = "\n".join(docs[:4])

        answer = generate_answer(context, final_question)

        return {
            "game_state": game_state,
            "strategy": answer
        }

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return {"error": str(e)}

@app.post("/guide")
def guide_newbie():
    try:
        question = "Tôi mới chơi TFT, hãy hướng dẫn tôi từ đầu"

        answer = generate_answer("", question)

        return {"guide": answer}

    except Exception as e:
        return {"error": str(e)}
