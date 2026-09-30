from ai_client import generate_text

async def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please enter a topic for your learning path.")
    return await generate_text(
        "Create a structured learning path for the topic below. Organize it from "
        "beginner to intermediate to advanced. Include prerequisite knowledge, "
        "ordered subtopics, a realistic suggested timeline, practice activities, "
        "and resource types (books, documentation, videos or articles). Do not invent "
        "specific URLs. Adapt the plan for a self-learner and clearly label estimates.\n\n"
        "Topic: " + topic
    )
