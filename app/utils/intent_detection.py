def rule_based_intent_detection(raw_input: str) -> tuple[str, float]:
    """Rule-based shortcuts for common intents before using the LLM."""
    text = raw_input.lower()

    if any(k in text for k in ["hi", "hello", "hey"]):
        return "greeting", 0.95

    if "summary" in text or "summarize" in text:
        return "summarization", 0.90

    if "search" in text or "find" in text:
        return "rag_query", 0.85

    if "code" in text or "bug" in text:
        return "coding_help", 0.85

    # Image prompts
    image_keywords = [
        "image", "picture", "photo", "render", "3d", "3d render",
        "generate", "generate an image", "art", "illustration",
        "digital art", "hd", "8k", "ultra-detailed", "cinematic lighting"
    ]
    if any(k in text for k in image_keywords):
        return "image_generation", 0.9

    if "task" in text or "do this" in text:
        return "task_request", 0.80

    return None, None