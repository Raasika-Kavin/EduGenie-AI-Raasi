import os
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="EduGenie", version="1.0.0",
              description="Google Gemini-powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class TaskRequest(BaseModel):
    task: Literal["explain", "qa", "quiz", "summarize", "learn"]
    text: str = Field(min_length=2, max_length=20000)
    level: str = Field(default="Beginner", max_length=40)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}

@app.post("/qa")
async def qa(payload: TaskRequest):
    return await run_task("qa", payload)

@app.post("/explain")
async def explain(payload: TaskRequest):
    return await run_task("explain", payload)

@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return await run_task("quiz", payload)

@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return await run_task("summarize", payload)

@app.post("/learn/recommendations")
async def learn(payload: TaskRequest):
    return await run_task("learn", payload)

async def run_task(task: str, payload: TaskRequest):
    if payload.task != task:
        raise HTTPException(status_code=400, detail=f"Send task='{task}' to this endpoint.")
    try:
        if task == "qa":
            result = await answer_question(payload.text, payload.level)
        elif task == "explain":
            result = await explain_concept(payload.text, payload.level)
        elif task == "quiz":
            result = await generate_quiz(payload.text, payload.level)
        elif task == "summarize":
            result = await summarize_text(payload.text)
        else:
            result = await get_learning_recommendations(payload.text, payload.level)
        return {"task": task, "result": result}
    except Exception as exc:
        # Do not expose credentials or provider internals to the browser.
        raise HTTPException(status_code=502, detail=f"AI request failed: {exc}") from exc
