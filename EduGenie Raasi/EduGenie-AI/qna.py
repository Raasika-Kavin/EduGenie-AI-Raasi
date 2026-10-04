from ai_client import generate

async def answer_question(question: str, level: str = "Beginner") -> str:
    prompt = f"""You are EduGenie, a careful educational tutor. Answer the question accurately
and clearly for a {level} learner. Use short paragraphs and bullets where useful.
If the question is ambiguous, state the assumption. Do not invent facts.
Question: {question}"""
    return await generate(prompt)
