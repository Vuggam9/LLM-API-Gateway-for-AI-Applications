import logging
from time import perf_counter

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.config import get_settings
from app.models.schemas import InferenceRequest, InferenceResponse, PromptListResponse
from app.services.auth import require_api_key
from app.services.cache import CacheService
from app.services.llm_service import LLMService
from app.services.metrics import metrics_store
from app.services.prompt_service import PromptService

router = APIRouter(prefix="/api/v1", tags=["inference"])
logger = logging.getLogger(__name__)

prompt_service = PromptService()
cache_service = CacheService()
llm_service = LLMService()


@router.get("/prompts", response_model=PromptListResponse, dependencies=[Depends(require_api_key)])
def list_prompts() -> PromptListResponse:
    return PromptListResponse(prompts=prompt_service.list_prompts())


@router.post("/infer", response_model=InferenceResponse, dependencies=[Depends(require_api_key)])
def run_inference(request: InferenceRequest, http_request: Request) -> InferenceResponse:
    try:
        prompt_text = prompt_service.render_prompt(request.template_name, request.input_variables)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except KeyError as exc:
        missing_key = str(exc).strip("'")
        raise HTTPException(
            status_code=400,
            detail=f"Missing input variable '{missing_key}' for template '{request.template_name}'.",
        ) from exc

    settings = get_settings()
    model_name = request.model_name or settings.openai_model
    cache_key = cache_service.build_cache_key(
        template_name=request.template_name,
        prompt_text=prompt_text,
        model_name=model_name,
        temperature=request.temperature,
    )

    request_id = getattr(http_request.state, "request_id", None)
    start_time = perf_counter()
    cached_response = cache_service.get(cache_key) if request.use_cache else None
    if cached_response is not None:
        latency_ms = (perf_counter() - start_time) * 1000
        metrics_store.record(latency_ms=latency_ms, cached=True, request_id=request_id)
        logger.info(
            "inference_completed | source=cache template=%s model=%s request_id=%s latency_ms=%.2f metadata=%s",
            request.template_name,
            model_name,
            request_id,
            latency_ms,
            request.metadata,
        )
        return InferenceResponse(
            response_text=cached_response,
            cached=True,
            latency_ms=latency_ms,
            template_name=request.template_name,
            model_name=model_name,
            request_id=request_id or "",
        )

    try:
        response_text = llm_service.generate(
            prompt_text=prompt_text,
            model_name=model_name,
            temperature=request.temperature,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if request.use_cache:
        cache_service.set(cache_key, response_text)

    latency_ms = (perf_counter() - start_time) * 1000
    metrics_store.record(latency_ms=latency_ms, cached=False, request_id=request_id)
    logger.info(
        "inference_completed | source=model template=%s model=%s request_id=%s latency_ms=%.2f metadata=%s",
        request.template_name,
        model_name,
        request_id,
        latency_ms,
        request.metadata,
    )
    return InferenceResponse(
        response_text=response_text,
        cached=False,
        latency_ms=latency_ms,
        template_name=request.template_name,
        model_name=model_name,
        request_id=request_id or "",
    )
