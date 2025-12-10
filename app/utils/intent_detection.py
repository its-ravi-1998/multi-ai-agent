def rule_based_intent_detection(raw_input: str) -> tuple[str, float]:
    """Rule based intent detection."""
    if any(k in raw_input for k in ["hi", "hello", "hey"]):
        return "greeting", 0.95
    if "summary" in raw_input or "summarize" in raw_input:
        return "summarization", 0.90

    if "search" in raw_input or "find" in raw_input:
        return "rag_query", 0.85

    if "code" in raw_input or "bug" in raw_input:
        return "coding_help", 0.85

    if "task" in raw_input or "do this" in raw_input:
        return "task_request", 0.80
    return None, None