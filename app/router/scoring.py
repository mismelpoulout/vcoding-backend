class ModelScore:
    def __init__(self, quality: float, latency: float, error_rate: float, cost: float):
        self.quality = quality
        self.latency = latency
        self.error_rate = error_rate
        self.cost = cost

def compute_score(model_stats: ModelScore, weights: dict) -> float:
    """
    Computes a dynamic score based on current model statistics and weights.
    Higher is better.
    """
    return (
        weights.get("quality", 1.0) * model_stats.quality
        - weights.get("latency", 0.1) * model_stats.latency
        - weights.get("error", 10.0) * model_stats.error_rate
        - weights.get("cost", 0.5) * model_stats.cost
    )

# Mocked dynamic stats for testing - in production this comes from Prometheus/Redis metrics
DYNAMIC_STATS = {
    "gemini-pro": ModelScore(quality=0.85, latency=1.2, error_rate=0.01, cost=0.0), # Free first strategy
    "gpt-4-turbo": ModelScore(quality=0.98, latency=2.0, error_rate=0.005, cost=0.05),
    "deepseek-coder": ModelScore(quality=0.90, latency=1.5, error_rate=0.02, cost=0.005),
}

def rank_models(task: str) -> list[str]:
    # Weights could be adjusted based on task (e.g. debugging needs high quality, basic code gen is fine with lower cost)
    weights = {"quality": 1.0, "latency": 0.5, "error": 5.0, "cost": 2.0}
    
    if task == "debugging":
        weights = {"quality": 2.0, "latency": 0.1, "error": 5.0, "cost": 0.5} # Prefer quality
    elif task == "documentation":
        weights = {"quality": 0.5, "latency": 1.0, "error": 2.0, "cost": 5.0} # Prefer cheap/fast
        
    scored = []
    for model_id, stats in DYNAMIC_STATS.items():
        score = compute_score(stats, weights)
        scored.append((score, model_id))
        
    # Sort descending (highest score first)
    scored.sort(reverse=True, key=lambda x: x[0])
    return [model_id for _, model_id in scored]
