import json
from ai_client import generate_text

def clean_json_block(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
    return text.strip()

async def generate_quiz(source: str) -> list[dict]:
    source = source.strip()
    if not source:
        raise ValueError("Enter a topic or passage to generate a quiz.")
    prompt = f"""Create exactly 3 educational multiple-choice questions based on the topic or passage below.
Return only a JSON array. Each item must have:
"question": string,
"options": an array of exactly 4 strings,
"answer": the exact text of the correct option,
"explanation": a short explanation.
Do not include markdown fences. Ensure there is one unambiguous correct answer.

Source:
{source}"""
    raw = clean_json_block(await generate_text(prompt, json_mode=True))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse quiz JSON: {exc}") from exc
    if isinstance(data, dict):
        data = data.get("questions", [])
    if not isinstance(data, list) or len(data) != 3:
        raise RuntimeError("Gemini did not return exactly three quiz questions.")
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("question"), str):
            raise RuntimeError("Quiz response has an invalid question structure.")
        options = item.get("options")
        if not isinstance(options, list) or len(options) != 4:
            raise RuntimeError("Each quiz question must have exactly four options.")
        if item.get("answer") not in options:
            raise RuntimeError("A quiz answer did not match one of its options.")
        item.setdefault("explanation", "")
    return data
