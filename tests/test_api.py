from fastapi.testclient import TestClient
from main import app
import main
from gemini_client import GeminiServiceError

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert 'EduGenie' in response.text

def test_qa(monkeypatch):
    monkeypatch.setattr(main, 'answer_question', lambda question, context='': 'Test answer')
    response = client.post('/qa', json={'text': 'What is AI?'})
    assert response.status_code == 200
    assert response.json()['answer'] == 'Test answer'

def test_gemini_service_error_returns_json(monkeypatch):
    def fail_request(question, context=''):
        raise GeminiServiceError('Gemini is temporarily busy. Please try again shortly.')

    monkeypatch.setattr(main, 'answer_question', fail_request)
    response = client.post('/qa', json={'text': 'What is AI?'})
    assert response.status_code == 503
    assert response.json()['detail'] == 'Gemini is temporarily busy. Please try again shortly.'

def test_explain(monkeypatch):
    monkeypatch.setattr(main, 'explain_topic', lambda text: 'Simple explanation')
    response = client.post('/explain', json={'text': 'Photosynthesis'})
    assert response.status_code == 200
    assert response.json()['explanation'] == 'Simple explanation'
