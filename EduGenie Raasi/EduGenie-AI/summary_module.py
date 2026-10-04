from ai_client import generate

async def summarize_text(text: str) -> str:
    return await generate(f"""Summarize the educational passage below for quick revision.
Preserve its important facts and meaning. Use a concise title and 4-7 bullet points.
Do not add information that is not in the passage.
PASSAGE:
{text}""")
