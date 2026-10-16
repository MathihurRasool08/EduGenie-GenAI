import pytest
from google.genai.errors import APIError

import gemini_client


class FakeModels:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = 0

    def generate_content(self, **kwargs):
        self.calls += 1
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


class FakeClient:
    def __init__(self, responses):
        self.models = FakeModels(responses)


def unavailable_error():
    return APIError(
        503,
        {"error": {"code": 503, "message": "Temporarily unavailable", "status": "UNAVAILABLE"}},
    )


def test_generate_text_retries_temporary_gemini_error(monkeypatch):
    client = FakeClient([unavailable_error(), type("Response", (), {"text": "Answer"})()])
    sleeps = []
    monkeypatch.setattr(gemini_client, "get_client", lambda: client)
    monkeypatch.setattr(gemini_client.time, "sleep", sleeps.append)

    assert gemini_client.generate_text("Question") == "Answer"
    assert client.models.calls == 2
    assert sleeps == [1]


def test_generate_text_reports_gemini_still_busy(monkeypatch):
    client = FakeClient([unavailable_error(), unavailable_error()])
    monkeypatch.setattr(gemini_client, "get_client", lambda: client)
    monkeypatch.setattr(gemini_client.time, "sleep", lambda _: None)

    with pytest.raises(gemini_client.GeminiServiceError, match="temporarily busy"):
        gemini_client.generate_text("Question")

    assert client.models.calls == 2
