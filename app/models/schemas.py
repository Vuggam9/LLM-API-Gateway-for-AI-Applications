from typing import Any

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    template_name: str = Field(..., description="Prompt template filename without extension.")
    input_variables: dict[str, Any] = Field(default_factory=dict)
    model_name: str | None = Field(default=None, description="Optional override model name.")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    use_cache: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class InferenceResponse(BaseModel):
    response_text: str
    cached: bool
    latency_ms: float
    template_name: str
    model_name: str
    request_id: str


class PromptListResponse(BaseModel):
    prompts: list[str]


class MetricsResponse(BaseModel):
    total_requests: int
    cache_hits: int
    cache_misses: int
    average_latency_ms: float
    last_request_id: str | None


class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
