"""Shared Gemini client. Configure GEMINI_API_KEY and GEMINI_MODEL in .env."""
import os
from functools import lru_cache
from google import genai
from google.genai import types

@lru_cache(maxsize=1)
def get_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your_gemini_api_key_here":
        raise RuntimeError("Gemini API key missing. Add GEMINI_API_KEY to .env.")
    return genai.Client(api_key=key)

async def generate(prompt: str, *, json_mode: bool = False) -> str:
    client = get_client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    config = types.GenerateContentConfig(
        temperature=0.4,
        response_mime_type="application/json" if json_mode else "text/plain",
    )
    response = await client.aio.models.generate_content(
        model=model, contents=prompt, config=config
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("The AI provider returned an empty response.")
    return text
