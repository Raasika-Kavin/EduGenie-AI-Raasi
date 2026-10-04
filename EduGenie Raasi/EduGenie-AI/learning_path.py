from ai_client import generate

async def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    return await generate(f"""Create a practical learning path for: {topic}
Learner's current level: {level}.
Organize it from beginner to intermediate to advanced. Include a suggested timeline,
specific topics in order, practice tasks, milestones, and useful resource types
(books, documentation, videos). Do not fabricate URLs or claim a resource is verified.
Make the plan encouraging and realistic.""")
