import json
from hashlib import sha256

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import get_settings


class CacheService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = Redis.from_url(settings.redis_url, decode_responses=True)
        self.ttl_seconds = settings.cache_ttl_seconds

    @staticmethod
    def build_cache_key(template_name: str, prompt_text: str, model_name: str, temperature: float) -> str:
        raw_key = json.dumps(
            {
                "template_name": template_name,
                "prompt_text": prompt_text,
                "model_name": model_name,
                "temperature": temperature,
            },
            sort_keys=True,
        )
        return f"llm_gateway:{sha256(raw_key.encode('utf-8')).hexdigest()}"

    def get(self, key: str) -> str | None:
        try:
            return self.client.get(key)
        except RedisError:
            return None

    def set(self, key: str, value: str) -> None:
        try:
            self.client.setex(key, self.ttl_seconds, value)
        except RedisError:
            return

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except RedisError:
            return False
