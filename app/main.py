from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import structlog

from .models.schemas import AIRequest, AIResponse
from .router.router import router
from .router.classifier import classify_task

logger = structlog.get_logger()
app = FastAPI(title="AI Forge Editor Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request processed", path=request.url.path, method=request.method, duration=process_time)
    return response

@app.post("/ai/generate", response_model=AIResponse)
async def generate(req: AIRequest):
    try:
        task_classified = classify_task(req.prompt, req.context)
        
        config = req.config
        if req.force_model:
            config["force_model"] = req.force_model
            
        response_text, model_used, latency = await router.route(req.prompt, config)
        
        return AIResponse(
            response=response_text,
            model_used=model_used,
            latency_ms=latency,
            task_classified=task_classified
        )
    except Exception as e:
        logger.error("Generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/status")
async def model_status():
    from .router.scoring import DYNAMIC_STATS
    return {"status": "ok", "models": [k for k in DYNAMIC_STATS.keys()]}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
