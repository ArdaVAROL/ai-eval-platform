import time

from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import AppError
from app.models.dataset import Dataset
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.prompt_version import PromptVersion
from app.schemas.experiment import ExperimentCreate
from app.services import OllamaLLMClient, evaluate_output


def create(db: Session, payload: ExperimentCreate) -> Experiment:
    dataset = db.get(Dataset, payload.dataset_id)
    if dataset is None:
        raise AppError(status.HTTP_404_NOT_FOUND, "Dataset not found.")

    prompt_version = db.get(PromptVersion, payload.prompt_version_id)
    if prompt_version is None:
        raise AppError(status.HTTP_404_NOT_FOUND, "Prompt version not found.")

    experiment = Experiment(**payload.model_dump())
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment


def list_all(db: Session) -> list[Experiment]:
    statement = (
        select(Experiment)
        .options(selectinload(Experiment.dataset), selectinload(Experiment.prompt_version))
        .order_by(Experiment.created_at.desc())
    )
    return list(db.scalars(statement).all())


def _build_model_input(prompt_text: str, test_case_input: str) -> str:
    return (
        "You are running an evaluation task.\n\n"
        f"Prompt:\n{prompt_text.strip()}\n\n"
        f"Test case input:\n{test_case_input.strip()}\n"
    )


def run_experiment(db: Session, experiment_id: int) -> list[ExperimentRun] | None:
    experiment = db.scalar(
        select(Experiment)
        .options(
            selectinload(Experiment.dataset).selectinload(Dataset.test_cases),
            selectinload(Experiment.prompt_version),
        )
        .where(Experiment.id == experiment_id)
    )
    if experiment is None:
        return None
    if not experiment.dataset.test_cases:
        raise AppError(
            status.HTTP_400_BAD_REQUEST,
            "This experiment's dataset has no test cases. Add test cases before triggering a run.",
        )

    llm_client = OllamaLLMClient()
    created_runs: list[ExperimentRun] = []
    prompt_text = experiment.prompt_version.prompt_text

    for test_case in experiment.dataset.test_cases:
        model_input = _build_model_input(prompt_text, test_case.input_text)
        started_at = time.perf_counter()
        llm_response = llm_client.generate(model_input)
        latency_ms = int((time.perf_counter() - started_at) * 1000)
        passed, score = evaluate_output(llm_response.output_text, test_case.expected_output)

        run = ExperimentRun(
            experiment_id=experiment.id,
            test_case_id=test_case.id,
            output_text=llm_response.output_text,
            latency_ms=latency_ms,
            prompt_tokens=llm_response.prompt_tokens,
            completion_tokens=llm_response.completion_tokens,
            total_tokens=llm_response.total_tokens,
            cost_usd=0.0,
            passed=passed,
            score=score,
        )
        db.add(run)
        created_runs.append(run)

    db.commit()
    for run in created_runs:
        db.refresh(run)
    return created_runs
