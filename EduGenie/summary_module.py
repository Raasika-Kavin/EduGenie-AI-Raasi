from ai_client import generate_text

async def summarize_text(source: str) -> str:
    source = source.strip()
    if not source:
        raise ValueError("Please enter text to summarize.")
    return await generate_text(
        "Summarize the following educational text for quick revision. Preserve the "
        "main ideas and important facts, remove repetition, and use clear concise "
        "language. Do not add facts not present in the source.\n\nText:\n" + source
    )
