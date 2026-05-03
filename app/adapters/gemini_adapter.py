from .base import BaseModelAdapter
from typing import Dict, Any
import httpx
from ..core.config import settings

class GeminiAdapter(BaseModelAdapter):
    def __init__(self, model_id: str = "gemini-pro"):
        super().__init__(model_id)
        self.api_key = settings.GEMINI_API_KEY

    async def generate(self, prompt: str, config: Dict[str, Any]) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set")
            
        timeout = config.get("timeout", 30.0)
        base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                raise ValueError(f"Unexpected response format from Gemini: {data}")
