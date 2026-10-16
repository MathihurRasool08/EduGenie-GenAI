from functools import lru_cache
import time

from config import settings

class GeminiServiceError(RuntimeError):
    pass

@lru_cache
def get_client():
    from google import genai
    from google.genai import types

    if not settings.gemini_api_key:
        raise GeminiServiceError("GEMINI_API_KEY is not configured. Add it to the .env file.")
    return genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(timeout=60000),
    )

def generate_text(prompt: str, *, temperature: float | None = None, response_schema=None) -> str:
    from google.genai import errors, types

    try:
        config_kwargs = {
            "temperature": settings.gemini_temperature if temperature is None else temperature,
        }
        if response_schema is not None:
            config_kwargs.update({
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            })
        for attempt in range(2):
            try:
                response = get_client().models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config_kwargs),
                )
                break
            except errors.APIError as exc:
                if exc.code not in (429, 500, 502, 503, 504):
                    raise GeminiServiceError(
                        f"Gemini request failed (HTTP {exc.code}): {exc.message or 'Unknown API error.'}"
                    ) from exc
                if attempt == 1:
                    raise GeminiServiceError(
                        "Gemini is temporarily busy. Please try again shortly."
                    ) from exc
                time.sleep(1)

        text = (response.text or "").strip()
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")
        return text
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini request failed: {exc}") from exc
