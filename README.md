# LLM API Gateway for AI Applications

This project is an internal-style API layer for LLM-powered applications. The main idea was to avoid having every app integrate with a model provider differently and instead expose one consistent FastAPI service for prompts, caching, auth, and request tracking.

## What I Focused On

I wanted this project to feel like a small platform component rather than a chatbot demo. The focus is on operational concerns around LLM usage: who can call the service, how prompts are reused, how repeated requests are cached, and how requests are observed.

The project covers:

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

## Tradeoffs And Limitations

- The metrics layer is intentionally lightweight and not backed by a full monitoring stack.
- Redis is used as a local caching dependency, but the project does not include more advanced cache invalidation or eviction policies.
- The gateway focuses on request orchestration and does not attempt multi-provider routing logic.

## What I Learned

The main takeaway from this project was that LLM application work quickly becomes backend engineering work. Prompt quality matters, but so do latency, repeated-call cost, authentication boundaries, and request visibility.

## Resume Bullet

Built a FastAPI-based LLM gateway with API key authentication, reusable prompt templates, Redis-backed response caching, OpenAI integration, and request-level observability to standardize and monitor LLM usage across internal AI workflows.
