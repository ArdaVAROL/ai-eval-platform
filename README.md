# AI Eval Platform

AI Eval Platform is a production-style MVP for evaluating prompt and model outputs across latency, local-model token usage, and pass/fail scoring. It is designed to be small enough to explain clearly in an interview while still showing real backend structure, data modeling, API design, migrations, and frontend integration.

## Project Overview

This project helps teams organize prompt evaluation workflows around a few core resources:

- `Datasets` group related evaluation inputs
- `Test cases` define individual prompts and expected outputs
- `Prompt versions` store prompt templates over time
- `Experiments` connect a dataset, a prompt version, and a target model
- `Experiment runs` store run-level output, latency, token counts, cost, and pass/fail results

The current backend runs experiments against a local Ollama model through the OpenAI Python SDK configured to use Ollama's OpenAI-compatible endpoint.

## Architecture Summary

The application is split into two simple layers:

- Backend: FastAPI app with SQLAlchemy models, Alembic migrations, CRUD modules, validation schemas, and REST endpoints
- Frontend: Next.js App Router UI with a small API utility layer and clean pages for datasets, prompt versions, experiments, and runs

High-level request flow:

1. The frontend sends requests to the FastAPI API.
2. FastAPI validates request payloads with Pydantic schemas.
3. CRUD modules interact with PostgreSQL through SQLAlchemy sessions.
4. Alembic manages schema evolution.
5. The dashboard consumes both list endpoints and a lightweight metrics summary endpoint.

## Stack

- Backend: Python 3.12, FastAPI
- Database: PostgreSQL by default, SQLite fallback for local development
- ORM: SQLAlchemy 2.x
- Migrations: Alembic
- Local model runtime: Ollama
- LLM client: OpenAI Python SDK pointed at `http://localhost:11434/v1`
- Frontend: Next.js, React, TypeScript
- Local config: environment variables via `.env` and `.env.local`

## Repository Structure

- [backend/app/main.py](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/app/main.py): FastAPI entrypoint
- [backend/app/api](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/app/api): route modules and API wiring
- [backend/app/crud](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/app/crud): database interaction logic
- [backend/app/models](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/app/models): SQLAlchemy models
- [backend/app/schemas](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/app/schemas): request and response schemas
- [backend/alembic](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/alembic): migration setup
- [frontend/app](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/frontend/app): Next.js routes
- [frontend/components](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/frontend/components): interview-friendly UI components
- [frontend/lib/api.ts](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/frontend/lib/api.ts): frontend API client
- [backend/sample_data/sample_eval_dataset.json](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/sample_data/sample_eval_dataset.json): sample data for demos

## Setup

### 1. Backend setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
Copy-Item .env.example .env
```

Update `.env` with your database settings and local Ollama settings. PostgreSQL is the default. For a local SQLite fallback:

```env
DATABASE_URL=sqlite:///./backend/ai_eval_platform.db
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.1
OLLAMA_API_KEY=ollama
```

Make sure Ollama is running locally and the model is available:

```powershell
ollama pull llama3.1
ollama serve
```

Run migrations:

```powershell
cd backend
alembic upgrade head
cd ..
```

Start the backend:

```powershell
uvicorn app.main:app --app-dir backend --reload
```

### 2. Optional sample seed data

The repository includes a small demo dataset in [backend/sample_data/sample_eval_dataset.json](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/backend/sample_data/sample_eval_dataset.json).

Seed it into the local database with:

```powershell
cd backend
python -m app.scripts.seed_sample_data
cd ..
```

### 3. Frontend setup

```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Default frontend API target:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Open `http://localhost:3000`.

## Local Development Commands

A simple [Makefile](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/Makefile) is included for common tasks:

```bash
make backend-install
make backend-migrate
make backend-run
make backend-seed
make frontend-install
make frontend-run
```

If `make` is not available on your machine, the equivalent manual commands are the setup commands shown above.

## Frontend Pages

- `/`: dashboard with snapshot metrics and evaluation summary
- `/datasets`: create datasets and test cases, view dataset table
- `/prompt-versions`: create prompt versions and review prompt text
- `/experiments`: create experiments and trigger local Ollama experiment runs
- `/runs`: inspect run records, latency, estimated cost, and pass/fail status

## API Endpoints

### Health

- `GET /health`

### Datasets

- `POST /api/v1/datasets`
- `GET /api/v1/datasets`

### Test Cases

- `POST /api/v1/test-cases`
- `GET /api/v1/test-cases`

### Prompt Versions

- `POST /api/v1/prompt-versions`
- `GET /api/v1/prompt-versions`

### Experiments

- `POST /api/v1/experiments`
- `GET /api/v1/experiments`
- `POST /api/v1/experiments/{experiment_id}/run`

### Runs

- `GET /api/v1/runs`

### Metrics

- `GET /api/v1/metrics/summary`

## Validation and Error Handling

The backend keeps validation intentionally simple and explicit:

- Pydantic field constraints reject empty or malformed payloads
- Duplicate dataset names and duplicate prompt version pairs return `409 Conflict`
- Missing related resources return `404 Not Found`
- Triggering a run without test cases returns `400 Bad Request`
- The API uses response models for health, resource lists, experiment run results, and metrics summaries

## Real Local LLM Flow

When you call `POST /api/v1/experiments/{experiment_id}/run`, the backend now:

1. Loads the experiment, linked dataset, dataset test cases, and selected prompt version.
2. Combines the prompt text and each test case input into one model input.
3. Calls Ollama at `http://localhost:11434/v1` using the OpenAI Python SDK.
4. Stores the model output, latency, token counts when available, zero local cost, and a deterministic pass/fail result.

The evaluation rule is intentionally simple and interview-friendly:

- normalize both the model output and `expected_output`
- pass when the expected text is contained in the output, or when token overlap / string similarity is high enough
- otherwise mark the run as failed

## Screenshots

Add screenshots to [docs/screenshots](/c:/Users/arda_/Desktop/Yazılım/python/ai-portfolio/01-eval-platform/docs/screenshots) and replace the placeholders below when you are ready:

![Dashboard Placeholder](docs/screenshots/dashboard-placeholder.png)
![Datasets Placeholder](docs/screenshots/datasets-placeholder.png)
![Runs Placeholder](docs/screenshots/runs-placeholder.png)

## Why This Is Interview-Friendly

- Clear separation between routes, schemas, models, and CRUD logic
- Small enough to explain quickly without hiding core engineering decisions
- Covers practical concerns: config, migrations, validation, metrics, and frontend integration
- Avoids premature complexity such as auth, queues, Redis, and background workers

## Future Improvements

- Add async/background execution for longer-running evaluations
- Support richer scoring methods beyond pass/fail placeholders
- Add filtering, pagination, and dataset/test case detail views
- Add automated tests for API routes and validation flows
- Add authentication and multi-user project/workspace support
- Add charts and historical trend analysis for runs and cost

## Notes

- The MVP defaults to PostgreSQL but supports SQLite for local fallback
- Docker services are assumed to be managed outside this folder
- The frontend is intentionally minimal and prioritizes clarity over design complexity
