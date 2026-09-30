from pathlib import Path
from typing import Any
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", description="Google Gemini-powered learning assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class TaskRequest(BaseModel):
    task: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=30000)

class TaskResponse(BaseModel):
    task: str
    result: Any

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}

@app.post("/qa", response_model=TaskResponse)
async def qa(payload: TaskRequest):
    return await run_task("qa", payload.text)

@app.post("/explain", response_model=TaskResponse)
async def explain(payload: TaskRequest):
    return await run_task("explain", payload.text)

@app.post("/quiz", response_model=TaskResponse)
async def quiz(payload: TaskRequest):
    return await run_task("quiz", payload.text)

@app.post("/summarize", response_model=TaskResponse)
async def summarize(payload: TaskRequest):
    return await run_task("summarize", payload.text)

@app.post("/learn/recommendations", response_model=TaskResponse)
async def recommendations(payload: TaskRequest):
    return await run_task("learn", payload.text)

async def run_task(task: str, text: str):
    handlers = {
        "qa": answer_question,
        "explain": explain_concept,
        "quiz": generate_quiz,
        "summarize": summarize_text,
        "learn": get_learning_recommendations,
    }
    try:
        result = await handlers[task](text)
        return {"task": task, "result": result}
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
    except Exception:
        logger.exception("Task failed: %s", task)
        return JSONResponse(status_code=502, content={"detail": "The AI service could not complete the request. Check the server logs and API configuration."})
