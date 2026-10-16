import json
from schemas import QuizResponse
from gemini_client import generate_text

QUIZ_SCHEMA = QuizResponse.model_json_schema()

def generate_quiz(text: str) -> QuizResponse:
    prompt = f"""Create exactly 3 multiple-choice questions from the educational content below.\nReturn JSON matching this schema exactly:\n{json.dumps(QUIZ_SCHEMA, indent=2)}\n\nRules:\n- Exactly 3 questions.\n- Exactly 4 options per question.\n- correct_answer must exactly match one option.\n- Include a short explanation for the correct answer.\n- Questions must be answerable from the supplied content.\n\nCONTENT:\n{text}"""
    raw = generate_text(prompt, temperature=0.2, response_schema=QUIZ_SCHEMA)
    try:
        return QuizResponse.model_validate_json(raw)
    except Exception as exc:
        raise ValueError(f"Quiz JSON validation failed: {exc}") from exc
