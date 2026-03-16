from fastapi import APIRouter

from app.api.routes import datasets, experiments, metrics, prompt_versions, runs, test_cases

api_router = APIRouter()
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(test_cases.router, prefix="/test-cases", tags=["test-cases"])
api_router.include_router(
    prompt_versions.router,
    prefix="/prompt-versions",
    tags=["prompt-versions"],
)
api_router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
