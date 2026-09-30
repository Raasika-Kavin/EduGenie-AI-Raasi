# EduGenie — Google Gemini-powered Learning Assistant

EduGenie is a FastAPI web application with a responsive HTML/CSS/JavaScript interface. It supports:
- Q&A (`/qa`)
- Beginner-friendly concept explanations (`/explain`)
- Three-question MCQ quizzes (`/quiz`)
- Text summaries (`/summarize`)
- Structured learning paths (`/learn/recommendations`)

The supplied project document specifies Gemini for Q&A, quizzes, summaries, and learning paths, and LaMini-Flan-T5-783M for explanations. The local model is optional; by default, explanations use Gemini so the application starts without downloading large model weights. Enable the local model in `.env` if desired.

## Requirements
- Python 3.10 or newer
- A Google AI Studio Gemini API key for AI features
- VS Code (recommended)

## Setup in VS Code

1. Extract the project folder and open `EduGenie` in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   py -3.10 -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   If installing PyTorch is not supported on your device, remove the optional `transformers`, `torch`, and `sentencepiece` lines from `requirements.txt`; Gemini mode still works.

5. Copy `.env.example` to `.env` and add your API key:
   - Windows: `Copy-Item .env.example .env`
   - macOS/Linux: `cp .env.example .env`

   Edit `.env` and replace `GEMINI_API_KEY` with your key. Never commit or share `.env`.

6. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
7. Open http://127.0.0.1:8000 in your browser. API documentation is at http://127.0.0.1:8000/docs.

## Test

Check server health:
```bash
curl http://127.0.0.1:8000/health
```

Try each API (replace sample text as needed):
```bash
curl -X POST http://127.0.0.1:8000/qa -H "Content-Type: application/json" -d "{\\"task\\":\\"qa\\",\\"text\\":\\"Which is the largest ocean?\\"}"
curl -X POST http://127.0.0.1:8000/explain -H "Content-Type: application/json" -d "{\\"task\\":\\"explain\\",\\"text\\":\\"Pythagoras theorem\\"}"
curl -X POST http://127.0.0.1:8000/quiz -H "Content-Type: application/json" -d "{\\"task\\":\\"quiz\\",\\"text\\":\\"The water cycle includes evaporation, condensation, and precipitation.\\"}"
curl -X POST http://127.0.0.1:8000/summarize -H "Content-Type: application/json" -d "{\\"task\\":\\"summarize\\",\\"text\\":\\"Paste an educational paragraph here.\\"}"
curl -X POST http://127.0.0.1:8000/learn/recommendations -H "Content-Type: application/json" -d "{\\"task\\":\\"learn\\",\\"text\\":\\"SQL\\"}"
```

You can also test all five tasks from the web interface. The quiz UI lets you select answers and checks them locally.

## Notes
- AI endpoints require a valid API key and internet access.
- Gemini model availability and quotas depend on your Google AI Studio account. Change `GEMINI_MODEL` if needed.
- The local LaMini model downloads weights on first use and can require substantial disk space and RAM. CPU inference may be slow.
- AI-generated material can contain errors; verify important academic facts.
