# EduGenie — Gemini-powered Learning Assistant

A FastAPI + HTML/CSS/JavaScript application implementing the five functions in the supplied project document: explain, Q&A, quiz, summarize, and learning recommendations.

## Requirements
- Python 3.10+
- A Gemini API key from https://aistudio.google.com/apikey
- VS Code (recommended)

The supplied document names Gemini 1.5 Pro. This implementation defaults to `gemini-2.5-flash` because model availability changes; set `GEMINI_MODEL` in `.env` to a model enabled for your key.

## Windows / VS Code setup
1. Install Python 3.10 or newer from https://www.python.org/downloads/windows/. During setup, enable **Add python.exe to PATH**. Close and reopen VS Code.
2. Open this folder in VS Code (`File → Open Folder`).
3. Open the integrated terminal (`Terminal → New Terminal`).
4. In PowerShell, create and activate a virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If `py` is not recognized, reinstall Python and select the PATH option. If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.
5. Install packages:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. Copy `.env.example` to `.env`, then replace the placeholder with your Gemini API key. Never share or commit `.env`.
7. Start the server:
   ```powershell
   uvicorn main:app --reload
   ```
8. Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs

## macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
uvicorn main:app --reload
```

## Test
- Open the web page and select each task.
- Health check: `http://127.0.0.1:8000/health`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Example PowerShell API call:
  ```powershell
  $body = @{ task="qa"; text="Which is the largest ocean?"; level="Beginner" } | ConvertTo-Json
  Invoke-RestMethod -Uri http://127.0.0.1:8000/qa -Method Post -ContentType "application/json" -Body $body
  ```
  For the other endpoints use `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`, and set `task` to the matching value.

## Local LaMini option
By default, explanations use Gemini so the app runs without a multi-GB local model download. To use LaMini-Flan-T5-783M locally:
1. Install the optional dependencies by uncommenting `transformers` and `torch` in `requirements.txt`, then run `pip install -r requirements.txt`.
2. Set `USE_LOCAL_EXPLANATION=true` in `.env`.
3. Restart the server. First run downloads model files. If loading fails and `LOCAL_MODEL_FALLBACK=true`, Gemini is used instead.

## Project structure
```
EduGenie-AI/
├── main.py
├── ai_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## API contract
All POST endpoints accept JSON: `{"task":"...", "text":"...", "level":"Beginner"}`. `level` is optional.
- `POST /qa` → text answer
- `POST /explain` → text explanation
- `POST /quiz` → array of 3 MCQs
- `POST /summarize` → concise summary
- `POST /learn/recommendations` → structured learning path
