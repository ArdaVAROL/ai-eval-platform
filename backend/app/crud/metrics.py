from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.prompt_version import PromptVersion
from app.models.test_case import TestCase
from app.schemas.metrics import MetricsSummaryRead


def get_summary(db: Session) -> MetricsSummaryRead:
    dataset_count = db.scalar(select(func.count()).select_from(Dataset)) or 0
    test_case_count = db.scalar(select(func.count()).select_from(TestCase)) or 0
    prompt_version_count = db.scalar(select(func.count()).select_from(PromptVersion)) or 0
    experiment_count = db.scalar(select(func.count()).select_from(Experiment)) or 0
    run_count = db.scalar(select(func.count()).select_from(ExperimentRun)) or 0

    average_latency_ms = float(db.scalar(select(func.avg(ExperimentRun.latency_ms))) or 0)
    total_cost_usd = float(db.scalar(select(func.sum(ExperimentRun.cost_usd))) or 0)
    passed_runs = int(
        db.scalar(select(func.count()).select_from(ExperimentRun).where(ExperimentRun.passed.is_(True))) or 0
    )
    failed_runs = max(run_count - passed_runs, 0)

    return MetricsSummaryRead(
        dataset_count=dataset_count,
        test_case_count=test_case_count,
        prompt_version_count=prompt_version_count,
        experiment_count=experiment_count,
        run_count=run_count,
        average_latency_ms=average_latency_ms,
        total_cost_usd=total_cost_usd,
        passed_runs=passed_runs,
        failed_runs=failed_runs,
    )
