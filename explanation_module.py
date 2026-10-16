from functools import lru_cache
from config import settings
from gemini_client import generate_text

@lru_cache
def _local_pipeline():
    from transformers import pipeline
    return pipeline("text2text-generation", model=settings.local_explainer_model)

def explain_topic(topic: str) -> str:
    prompt = f"""You are EduGenie, a patient educational tutor. Explain the following topic to a beginner.\nTopic: {topic}\n\nRequirements:\n- Use simple language.\n- Start with a one-sentence definition.\n- Give 3-5 key points.\n- Include one intuitive example or analogy.\n- Avoid unnecessary jargon.\n- Keep it concise but complete."""
    if settings.use_local_explainer:
        try:
            result = _local_pipeline()(prompt, max_new_tokens=350, do_sample=False)[0]["generated_text"]
            return result.strip()
        except Exception:
            # A local model is optional; cloud generation keeps the feature usable if the model cannot load.
            pass
    return generate_text(prompt)
