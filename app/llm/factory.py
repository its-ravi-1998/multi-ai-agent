import httpx
from typing import List, Dict


class LLM:
    """Simple LLM client for LM Studio."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:1234", model: str = "google/gemma-3-4b"):
        self.base_url = base_url
        self.model = model
    
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send messages and get response."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" not in result or not result["choices"]:
                raise ValueError("No choices in LLM response")
            
            content = result["choices"][0]["message"].get("content", "")
            if not content:
                raise ValueError("Empty content in LLM response")
            
            return content



llm = LLM()