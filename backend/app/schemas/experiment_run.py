from pydantic import BaseModel

from app.schemas.base import TimestampedSchema


class ExperimentRunRead(TimestampedSchema):
    experiment_id: int
    test_case_id: int
    output_text: str
    latency_ms: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    passed: bool
    score: float


class ExperimentRunBatchResponse(BaseModel):
    experiment_id: int
    created_runs: int
    runs: list[ExperimentRunRead]
