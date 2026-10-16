import json
from schemas import LearningPathResponse
from gemini_client import generate_text

LEARNING_SCHEMA = LearningPathResponse.model_json_schema()

def get_learning_recommendations(topic: str, learner_level: str = "beginner", goal: str = "build a strong foundation") -> LearningPathResponse:
    prompt = f"""Create a personalized learning path for the topic: {topic}.\nLearner level: {learner_level}\nGoal: {goal}\n\nReturn JSON matching this schema exactly:\n{json.dumps(LEARNING_SCHEMA, indent=2)}\n\nRules:\n- Progress from beginner to advanced where appropriate.\n- Make steps practical and ordered.\n- Give realistic estimated study times.\n- Resources may be generic resource types or well-known resource names; do not fabricate URLs.\n- Keep the plan useful to a self-learner."""
    raw = generate_text(prompt, temperature=0.3, response_schema=LEARNING_SCHEMA)
    try:
        return LearningPathResponse.model_validate_json(raw)
    except Exception as exc:
        raise ValueError(f"Learning-path JSON validation failed: {exc}") from exc
