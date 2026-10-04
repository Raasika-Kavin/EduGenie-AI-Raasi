"""Concept explanation. Uses the local LaMini model when enabled; otherwise Gemini."""
import os
from functools import lru_cache
from ai_client import generate

@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline
    model_name = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model_name, device=-1)

async def explain_concept(topic: str, level: str = "Beginner") -> str:
    if os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true":
        try:
            pipe = _local_pipeline()
            result = pipe(
                f"Explain {topic} to a {level} student in simple language with an example.",
                max_new_tokens=220, do_sample=False
            )
            return result[0]["generated_text"].strip()
        except Exception as exc:
            if os.getenv("LOCAL_MODEL_FALLBACK", "true").lower() != "true":
                raise RuntimeError(f"Local explanation model failed: {exc}") from exc
    prompt = f"""Explain the concept '{topic}' to a {level} learner using simple language.
Include: a one-sentence definition, how it works, one everyday example, and a brief recap.
Avoid unexplained jargon."""
    return await generate(prompt)
