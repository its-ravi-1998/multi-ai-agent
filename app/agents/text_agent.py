from app.llm.factory import llm as llm_factory
import json

async def text_agent(raw_input: str) -> str:
    """Text agent."""
    prompt = f"{raw_input}"
    response = await llm_factory.chat([
        {"role": "system", "content": "You are a text agent. You are responsible for generating text based on the user's input."},
        {"role": "user", "content": prompt}
    ])
    return response