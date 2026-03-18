from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)



def test_prompts_requires_api_key() -> None:
    response = client.get("/api/v1/prompts")
    assert response.status_code == 401



def test_health_is_public() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "redis_connected" in body
