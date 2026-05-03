from .base import BaseModelAdapter
from typing import Dict, Any
import httpx
from ..core.config import settings

class OpenAIAdapter(BaseModelAdapter):
    def __init__(self, model_id: str = "gpt-4-turbo"):
        super().__init__(model_id)
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def generate(self, prompt: str, config: Dict[str, Any]) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set")
            
        timeout = config.get("timeout", 30.0)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.get("temperature", 0.7)
        }
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
