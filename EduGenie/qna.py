from ai_client import generate_text

async def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")
    return await generate_text(
        "You are EduGenie, a careful educational assistant. Answer the student's "
        "question accurately and clearly. Use concise language, explain key terms, "
        "and say when you are uncertain.\n\nQuestion:\n" + question
    )
