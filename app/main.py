from fastapi import FastAPI

from app.core.logging_config import configure_logging
from app.middleware.request_context import RequestContextMiddleware
from app.routes.inference import router as inference_router
from app.routes.monitoring import router as monitoring_router

configure_logging()

app = FastAPI(
    title="LLM API Gateway",
    version="2.0.0",
    description="A production-style gateway for prompt-based LLM inference with auth, caching, and metrics.",
)

app.add_middleware(RequestContextMiddleware)
app.include_router(inference_router)
app.include_router(monitoring_router)
