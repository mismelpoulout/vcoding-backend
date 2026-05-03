import time
import structlog
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential
from .classifier import classify_task
from .scoring import rank_models
from ..adapters.openai_adapter import OpenAIAdapter
from ..adapters.gemini_adapter import GeminiAdapter
from ..adapters.deepseek_adapter import DeepseekAdapter

logger = structlog.get_logger()

class AIRouter:
    def __init__(self):
        self.adapters = {
            "gpt-4-turbo": OpenAIAdapter("gpt-4-turbo"),
            "gemini-pro": GeminiAdapter("gemini-pro"),
            "deepseek-coder": DeepseekAdapter("deepseek-coder")
        }

    async def route(self, prompt: str, config: Dict[str, Any]) -> tuple[str, str, float]:
        """
        Routes the prompt to the best model, applying fallbacks if needed.
        Returns (response_text, model_used, latency_ms)
        """
        task = classify_task(prompt, config.get("context"))
        
        # Determine target models
        force_model = config.get("force_model")
        if force_model and force_model in self.adapters:
            ranked_models = [force_model]
            logger.info("Using forced model", model=force_model)
        else:
            ranked_models = rank_models(task)
            logger.info("Ranked models for task", task=task, models=ranked_models)

        # Iterate over models as fallbacks
        for model_id in ranked_models:
            adapter = self.adapters.get(model_id)
            if not adapter:
                continue
                
            try:
                logger.info("Attempting generation", model=model_id)
                start_time = time.time()
                
                # We wrap the actual call in a retry mechanism specific to transient errors
                response = await self._generate_with_retry(adapter, prompt, config)
                
                latency = (time.time() - start_time) * 1000
                logger.info("Generation successful", model=model_id, latency_ms=latency)
                
                # Here we could asynchronously update the success stats in Redis
                return response, model_id, latency
                
            except Exception as e:
                logger.error("Model failed", model=model_id, error=str(e))
                # Update failure stats here to penalize this model dynamically
                continue
                
        raise Exception("All models failed or no suitable model found.")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _generate_with_retry(self, adapter, prompt: str, config: Dict[str, Any]) -> str:
        return await adapter.generate(prompt, config)

router = AIRouter()
