from app.utils.intent_detection import rule_based_intent_detection
from app.llm.factory import llm
import json
import re

INTENT_PROMPT = """
You are an intent classifier. Analyze the user input and classify it into one of these intents.

Available Intents:
1. greeting - User is greeting (hi, hello, hey, good morning, etc.)
2. task_request - User wants to perform a task or action (do this, complete, execute, etc.)
3. summarization - User wants to summarize something (summarize, summary, brief, etc.)
4. rag_query - User wants to search or find information (search, find, query, look for, etc.)
5. coding_help - User needs help with code, debugging, or programming (code, bug, error, fix, etc.)
6. agent_command - User is giving a command to control an agent (run agent, start, stop, etc.)
7. unknown - ONLY use this if the input doesn't fit any category above
8. image_generation - User wants to generate an image (generate image, create image, etc.)

IMPORTANT: 
- Try to classify into a specific intent. Only use "unknown" as a last resort.
- Be confident in your classification.
- Return ONLY valid JSON, no markdown, no code fences, no explanations.

Return format (JSON only):
{"intent": "intent_name", "confidence": 0.0-1.0}
"""


def extract_json_from_text(text: str) -> dict:
    """Extract JSON from text that might contain extra content."""
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")
    
    text = text.strip()

    # Remove code fences (```json ... ``` or ``` ... ```)
    # Handle both at start and anywhere in text
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'```\s*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
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
    prompt = f"{INTENT_PROMPT}\n\nUser input: {raw_input}\n\nReturn JSON only:"
    try:
        response = await llm.chat([
            {"role": "system", "content": "You are a JSON-only intent classifier. Always return valid JSON without markdown or code fences."},
            {"role": "user", "content": prompt}
        ])
        
        if not response:
            print("Warning: Empty response from LLM")
            return "unknown", 0.0
        
        print(f"LLM Response: {response[:200]}")  # Debug: log first 200 chars
        
        result = extract_json_from_text(response)
        print(result,"result from llm")
        
        intent = result.get("intent", "unknown")
        print(intent,"intent from llm")
        confidence = float(result.get("confidence", 0.0))
        
        return intent, confidence
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        # Fallback to unknown intent if LLM fails
        print(f"Error in LLM intent detection: {str(e)}")
        return "unknown", 0.0


async def intent_detection_agent(raw_input: str) -> tuple[str, float]:
    """Intent detection agent."""
    intent, confidence = rule_based_intent_detection(raw_input)
    print(intent, confidence,"rule based intent detection")
    if intent is None:
        print("LLM intent detection...")
        intent, confidence = await llm_intent_detection(raw_input)

    # Safeguard: if image-like keywords are present, force image_generation
    image_keywords = [
        "image", "picture", "photo", "render", "3d", "3d render",
        "generate", "generate an image", "art", "illustration",
        "digital art", "hd", "8k", "ultra-detailed", "cinematic lighting"
    ]
    text = raw_input.lower()
    if any(k in text for k in image_keywords):
        if intent != "image_generation":
            intent = "image_generation"
            confidence = max(confidence or 0.0, 0.9)
            print("Intent overridden to image_generation based on keywords")

    return intent, confidence