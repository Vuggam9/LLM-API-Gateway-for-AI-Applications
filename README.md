# LLM API Gateway for AI Applications

This project is a production-style API gateway for LLM-powered applications. It centralizes prompt handling, caching, authentication, and request observability behind a single FastAPI service.

## Why This Project Is Resume-Ready

This project reflects a realistic internal platform component that an AI/ML engineer might build to standardize LLM access across multiple applications.

It demonstrates:

- API design with FastAPI
- model access abstraction using LangChain and OpenAI
- Redis-based response caching to reduce cost and latency
- reusable prompt templates for workflow consistency
- API key authentication for service-to-service access
- request logging, correlation ids, and latency monitoring
- automated tests and Docker-based local setup

## Architecture

```text
Client / Internal App
        |
        v
FastAPI Gateway
  |-- API Key Auth
  |-- Request Middleware
  |-- Prompt Template Service
  |-- Redis Cache Service
  |-- LLM Service (OpenAI)
  `-- Metrics Store
```

## Setup

```powershell
cd "C:\Users\Maneesha Vuggam\Documents\New project\llm-api-gateway"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set these values in `.env`:

- `OPENAI_API_KEY`
- `API_KEYS`

Example:

```text
API_KEYS=local-dev-key,team-service-key
```

## Run Services

Start Redis:

```powershell
docker compose up redis -d
```

Run API locally:

```powershell
uvicorn app.main:app --reload
```

Or run everything with Docker:

```powershell
docker compose up --build
```

## Core Endpoints

- `GET /health`
- `GET /api/v1/prompts`
- `POST /api/v1/infer`
- `GET /api/v1/metrics`

Protected endpoints require:

```text
x-api-key: <your_api_key>
```

## Example Inference Request

```json
{
  "template_name": "summarize_text",
  "input_variables": {
    "text": "Redis caching reduces repeated LLM calls and improves latency."
  },
  "model_name": "gpt-4o-mini",
  "temperature": 0.2,
  "use_cache": true,
  "metadata": {
    "team": "support-automation",
    "workflow": "ticket-summary"
  }
}
```

## Testing

```powershell
pytest app/tests -q
```

## Resume Bullet

Built a FastAPI-based LLM gateway with API key authentication, reusable prompt templates, Redis-backed response caching, OpenAI integration, and request-level observability to standardize and monitor LLM usage across internal AI workflows.
