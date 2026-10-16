# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A (`POST /qa`)
- Concept explanation (`POST /explain`)
- 3-question MCQ quiz generation (`POST /quiz`)
- Educational summarization (`POST /summarize`)
- Beginner-to-advanced learning recommendations (`POST /learn/recommendations`)
- A responsive HTML/CSS browser interface
- Health check (`GET /health`)

The supplied documentation describes FastAPI, HTML/CSS, Jinja2, Gemini, and LaMini-Flan-T5, and specifies the five REST endpoints above. The implementation keeps that architecture. 

## Important model update

The source documentation names Gemini 1.5 Pro. This project reads the Gemini model from `.env` and defaults to `gemini-3.8-flash`, which is the model Google currently recommends for new usage. If your account does not expose that model, set `GEMINI_MODEL` to another currently available text model.

The documentation also names `LaMini-Flan-T5-783M` for explanations. To keep installation lightweight, the default is `USE_LOCAL_EXPLAINER=false`, so explanation uses Gemini. You can enable the original local-model approach with `requirements-local.txt` and `USE_LOCAL_EXPLAINER=true`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_api.py
```

## VS Code setup — Windows

### 1. Install Python

Use Python 3.10 or newer. Verify:

```powershell
python --version
```

### 2. Open the project

Extract/open the `EduGenie` folder in VS Code.

### 3. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Create the environment file

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

with your real Google AI Studio API key. Never commit `.env` to Git.

### 6. Run the application

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

The source documentation uses this same local Uvicorn workflow and address.

## API testing

### Health

```powershell
curl http://127.0.0.1:8000/health
```

### Q&A

```powershell
curl -X POST http://127.0.0.1:8000/qa `
  -H "Content-Type: application/json" `
  -d '{"text":"What is the largest ocean?"}'
```

### Explain

```powershell
curl -X POST http://127.0.0.1:8000/explain `
  -H "Content-Type: application/json" `
  -d '{"text":"Explain the Pythagoras theorem to a beginner."}'
```

### Quiz

```powershell
curl -X POST http://127.0.0.1:8000/quiz `
  -H "Content-Type: application/json" `
  -d '{"text":"The Earth revolves around the Sun and rotates on its axis."}'
```

### Summary

```powershell
curl -X POST http://127.0.0.1:8000/summarize `
  -H "Content-Type: application/json" `
  -d '{"text":"Paste a long educational paragraph here."}'
```

### Learning path

```powershell
curl -X POST http://127.0.0.1:8000/learn/recommendations `
  -H "Content-Type: application/json" `
  -d '{"text":"SQL"}'
```

## Automated tests

Tests mock Gemini-dependent functions so they do not consume API quota:

```powershell
pytest -q
```

## Optional LaMini local explanation

To use the model named in the documentation for the explanation module:

```powershell
pip install -r requirements-local.txt
```

Then set in `.env`:

```text
USE_LOCAL_EXPLAINER=true
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first use downloads the model from Hugging Face and can require significant disk space/RAM. If the local model cannot load, the application automatically falls back to Gemini.

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Check that `.env` exists in the project root and contains a valid key.

### Gemini model not found / unavailable
Change `GEMINI_MODEL` in `.env` to a model available to your Google AI Studio account.

### PowerShell execution policy
Use Command Prompt for activation, or configure your PowerShell execution policy according to your organization's rules.

### Port already in use
Run:

```powershell
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.
