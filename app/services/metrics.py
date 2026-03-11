from dataclasses import dataclass


@dataclass
class MetricsStore:
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    total_latency_ms: float = 0.0
    last_request_id: str | None = None

    def record(self, latency_ms: float, cached: bool, request_id: str | None) -> None:
        self.total_requests += 1
        self.total_latency_ms += latency_ms
        self.last_request_id = request_id
        if cached:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    @property
    def average_latency_ms(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_latency_ms / self.total_requests


metrics_store = MetricsStore()
