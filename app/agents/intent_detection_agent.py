from app.utils.intent_detection import rule_based_intent_detection
from app.llm.factory import llm
import json
import re

INTENT_PROMPT = """
You are an intent classifier. Return JSON only.

Intents:
- greeting
- task_request
- summarization
- rag_query
- coding_help
- agent_command
- unknown

Reply format:
{"intent": "...", "confidence": 0.0}
"""


def extract_json_from_text(text: str) -> dict:
    """Extract JSON from text that might contain extra content."""
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")
    
    # Try to find JSON object in the response
    json_match = re.search(r'\{[^{}]*"intent"[^{}]*"confidence"[^{}]*\}', text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    
    # Try direct JSON parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response from LLM: {text[:100]}")


async def llm_intent_detection(raw_input: str) -> tuple[str, float]:
    """LLM intent detection."""
    prompt = f"{INTENT_PROMPT}\n\nUser input: {raw_input}"
    try:
        response = await llm.chat([
            {"role": "user", "content": prompt}
        ])
        
        if not response:
            raise ValueError("Empty response from LLM")
        
        result = extract_json_from_text(response)
        
        intent = result.get("intent", "unknown")
        confidence = float(result.get("confidence", 0.0))
        
        return intent, confidence
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        # Fallback to unknown intent if LLM fails
        return "unknown", 0.0


async def intent_detection_agent(raw_input: str) -> tuple[str, float]:
    """Intent detection agent."""
    intent, confidence = rule_based_intent_detection(raw_input)
    if intent is None:
        intent, confidence = await llm_intent_detection(raw_input)
    return intent, confidence