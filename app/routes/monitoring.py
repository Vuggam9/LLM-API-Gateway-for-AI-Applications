from fastapi import APIRouter, Depends

from app.models.schemas import HealthResponse, MetricsResponse
from app.services.auth import require_api_key
from app.services.cache import CacheService
from app.services.metrics import metrics_store

router = APIRouter(tags=["monitoring"])
cache_service = CacheService()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    redis_connected = cache_service.ping()
    return HealthResponse(
        status="ok" if redis_connected else "degraded",
        redis_connected=redis_connected,
    )


@router.get("/api/v1/metrics", response_model=MetricsResponse, dependencies=[Depends(require_api_key)])
def get_metrics() -> MetricsResponse:
    return MetricsResponse(
        total_requests=metrics_store.total_requests,
        cache_hits=metrics_store.cache_hits,
        cache_misses=metrics_store.cache_misses,
        average_latency_ms=round(metrics_store.average_latency_ms, 2),
        last_request_id=metrics_store.last_request_id,
    )
