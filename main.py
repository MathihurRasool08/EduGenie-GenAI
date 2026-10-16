from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import settings
from gemini_client import GeminiServiceError
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import QARequest, TextRequest, QuizResponse, LearningPathResponse
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title=settings.app_name, version="1.0.0", description="Google Gemini powered learning assistant")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.exception_handler(GeminiServiceError)
async def gemini_service_error_handler(request: Request, exc: GeminiServiceError):
    return JSONResponse(status_code=503, content={"detail": str(exc)})

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "gemini_configured": bool(settings.gemini_api_key), "model": settings.gemini_model}

@app.post("/qa")
def qa(request: QARequest):
    question = request.question or request.text
    context = request.text if request.question else ""
    return {"answer": answer_question(question, context)}

@app.post("/explain")
def explain(request: TextRequest):
    return {"explanation": explain_topic(request.text)}

@app.post("/quiz", response_model=QuizResponse)
def quiz(request: TextRequest):
    return generate_quiz(request.text)

@app.post("/summarize")
def summarize(request: TextRequest):
    return {"summary": summarize_text(request.text)}

@app.post("/learn/recommendations", response_model=LearningPathResponse)
def recommendations(request: TextRequest):
    return get_learning_recommendations(request.text)
