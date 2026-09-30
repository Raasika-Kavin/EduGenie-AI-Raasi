"""Concept explanation using LaMini-Flan-T5 locally, with Gemini fallback.

The local model is optional because it is large and can be slow on first download.
Set USE_LOCAL_EXPLAINER=true to enable it. If unavailable, Gemini is used.
"""
import os
from functools import lru_cache
from ai_client import generate_text

@lru_cache(maxsize=1)
def _load_local_model():
    from transformers import pipeline
    model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model_name, device=-1)

async def explain_concept(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please enter a topic to explain.")
    if os.getenv("USE_LOCAL_EXPLAINER", "false").lower() in {"1", "true", "yes"}:
        try:
            model = _load_local_model()
            output = model(
                "Explain this concept to a beginner in simple language: " + topic,
                max_new_tokens=220, do_sample=False
            )
            if output and output[0].get("generated_text"):
                return output[0]["generated_text"].strip()
        except Exception:
            # A missing model/dependency should not make the whole application unusable.
            pass
    return await generate_text(
        "Explain the following concept to a beginner. Use simple language, a short "
        "example, and a brief recap. Avoid unnecessary jargon.\n\nTopic:\n" + topic
    )
