import logging
import uuid
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        start_time = perf_counter()
        request.state.request_id = request_id

        response = await call_next(request)

        latency_ms = (perf_counter() - start_time) * 1000
        response.headers["x-request-id"] = request_id
        response.headers["x-process-time-ms"] = f"{latency_ms:.2f}"

        logger.info(
            "request_completed | method=%s path=%s status_code=%s request_id=%s latency_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            request_id,
            latency_ms,
        )
        return response
