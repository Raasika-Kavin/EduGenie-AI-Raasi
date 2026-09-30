"""Shared Gemini client and response helpers."""
import os
from functools import lru_cache
from google import genai
from google.genai import types

@lru_cache(maxsize=1)
def get_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise ValueError("GEMINI_API_KEY is not set. Add your Google AI Studio API key to .env.")
    return genai.Client(api_key=key)

def get_model() -> str:
    # Override in .env if your account uses a different available Gemini model.
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

async def generate_text(prompt: str, *, json_mode: bool = False) -> str:
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=0.4,
        response_mime_type="application/json" if json_mode else "text/plain",
    )
    response = await client.aio.models.generate_content(
        model=get_model(), contents=prompt, config=config
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
