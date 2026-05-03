from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModelAdapter(ABC):
    def __init__(self, model_id: str):
        self.model_id = model_id
        
    @abstractmethod
    async def generate(self, prompt: str, config: Dict[str, Any]) -> str:
        """
        Generates text given a prompt and config.
        Must handle API keys, errors, normalization, and timeouts.
        """
        pass
