import pytest
from app.router.classifier import classify_task
from app.router.scoring import compute_score, ModelScore, rank_models

def test_classify_task():
    assert classify_task("Please refactor this code") == "code_refactor"
    assert classify_task("Explain this function") == "documentation"
    assert classify_task("Translate this python to go") == "translation"
    assert classify_task("Write a fast sort algorithm") == "code_generation"

def test_compute_score():
    stats = ModelScore(quality=0.9, latency=1.0, error_rate=0.01, cost=0.0)
    weights = {"quality": 1.0, "latency": 0.1, "error": 10.0, "cost": 1.0}
    
    score = compute_score(stats, weights)
    # 0.9*1.0 - 1.0*0.1 - 0.01*10.0 - 0.0*1.0 = 0.9 - 0.1 - 0.1 - 0 = 0.7
    assert abs(score - 0.7) < 0.001

def test_rank_models():
    # Test that it prefers high quality for debugging
    ranked = rank_models("debugging")
    assert isinstance(ranked, list)
    assert len(ranked) > 0
    # gpt-4-turbo should rank high for debugging based on static values
    assert ranked[0] == "gpt-4-turbo"
