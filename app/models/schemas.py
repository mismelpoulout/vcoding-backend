from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class AIRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    task_type: Optional[str] = "auto"
    force_model: Optional[str] = None
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AIResponse(BaseModel):
    response: str
    model_used: str
    latency_ms: float
    task_classified: str
    tokens_used: Optional[int] = None
    
class ModelMetrics(BaseModel):
    quality: float
    latency: float
    error_rate: float
    cost: float
