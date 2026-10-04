import json
from ai_client import generate

async def generate_quiz(source: str, level: str = "Beginner") -> list[dict]:
    prompt = f"""Create exactly 3 multiple-choice questions based only on the source below,
suitable for a {level} learner. Return a JSON array. Each item must have:
"question" (string), "options" (array of exactly 4 strings),
"correct_answer" (one option string, exactly matching an option),
"explanation" (short string). Make distractors plausible.
SOURCE:
{source}"""
    raw = await generate(prompt, json_mode=True)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        # Defensive recovery if a provider wraps JSON despite JSON mode.
        start, end = raw.find("["), raw.rfind("]")
        if start < 0 or end <= start:
            raise ValueError(f"Could not parse quiz JSON: {raw[:500]}") from exc
        data = json.loads(raw[start:end + 1])
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Quiz response must contain exactly 3 questions.")
    for item in data:
        if not isinstance(item, dict) or len(item.get("options", [])) != 4:
            raise ValueError("Each quiz question must contain exactly 4 options.")
        if item.get("correct_answer") not in item["options"]:
            raise ValueError("Quiz correct_answer must match one of its options.")
    return data
