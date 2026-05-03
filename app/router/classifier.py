import re

def classify_task(prompt: str, context: str = None) -> str:
    """
    Classifies the prompt into predefined categories to aid model routing.
    """
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["refactor", "optimize", "clean"]):
        return "code_refactor"
    if any(word in prompt_lower for word in ["explain", "document", "docstring", "comment"]):
        return "documentation"
    if any(word in prompt_lower for word in ["translate", "convert"]):
        return "translation"
    if any(word in prompt_lower for word in ["test", "pytest", "unit test"]):
        return "testing"
    if any(word in prompt_lower for word in ["bug", "fix", "error", "traceback", "exception"]):
        return "debugging"
    
    # Default is general code generation
    return "code_generation"
