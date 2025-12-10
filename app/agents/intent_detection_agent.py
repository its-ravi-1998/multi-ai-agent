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
    
    text = text.strip()
    
    # Strategy 1: Try to find JSON object with balanced braces
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.finditer(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            json_str = match.group()
            # Try to parse it
            result = json.loads(json_str)
            if "intent" in result and "confidence" in result:
                return result
        except json.JSONDecodeError:
            continue
    
    # Strategy 2: Try to extract JSON with more flexible pattern
    # Look for content between first { and last }
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            json_str = text[first_brace:last_brace + 1]
            # Clean up common issues
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
            json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays
            result = json.loads(json_str)
            if "intent" in result and "confidence" in result:
                return result
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Try direct JSON parse
    try:
        result = json.loads(text)
        if "intent" in result and "confidence" in result:
            return result
    except json.JSONDecodeError:
        pass
    
    # If all strategies fail, raise error with context
    raise ValueError(f"Could not extract valid JSON from LLM response. Response: {text[:200]}")


async def llm_intent_detection(raw_input: str) -> tuple[str, float]:
    """LLM intent detection."""
    prompt = f"{INTENT_PROMPT}\n\nUser input: {raw_input}"
    try:
        response = await llm.chat([
            {"role": "user", "content": prompt}
        ])
        
        if not response:
            print("Warning: Empty response from LLM")
            return "unknown", 0.0
        
        print(f"LLM Response: {response[:200]}")  # Debug: log first 200 chars
        
        result = extract_json_from_text(response)
        
        intent = result.get("intent", "unknown")
        confidence = float(result.get("confidence", 0.0))
        
        return intent, confidence
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        # Fallback to unknown intent if LLM fails
        print(f"Error in LLM intent detection: {str(e)}")
        return "unknown", 0.0


async def intent_detection_agent(raw_input: str) -> tuple[str, float]:
    """Intent detection agent."""
    intent, confidence = rule_based_intent_detection(raw_input)
    if intent is None:
        print("LLM intent detection...")
        intent, confidence = await llm_intent_detection(raw_input)
    return intent, confidence