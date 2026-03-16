from pydantic import BaseModel


class MetricsSummaryRead(BaseModel):
    dataset_count: int
    test_case_count: int
    prompt_version_count: int
    experiment_count: int
    run_count: int
    average_latency_ms: float
    total_cost_usd: float
    passed_runs: int
    failed_runs: int
