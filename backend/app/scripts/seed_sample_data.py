import json
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.dataset import Dataset
from app.models.experiment import Experiment
from app.models.prompt_version import PromptVersion
from app.models.test_case import TestCase


def main() -> None:
    sample_path = Path(__file__).resolve().parents[2] / "sample_data" / "sample_eval_dataset.json"
    payload = json.loads(sample_path.read_text(encoding="utf-8"))

    with SessionLocal() as db:
        dataset_name = payload["dataset"]["name"]
        dataset = db.scalar(select(Dataset).where(Dataset.name == dataset_name))
        if dataset is None:
            dataset = Dataset(**payload["dataset"])
            db.add(dataset)
            db.flush()

        for test_case_payload in payload["test_cases"]:
            existing_test_case = db.scalar(
                select(TestCase).where(
                    TestCase.dataset_id == dataset.id,
                    TestCase.input_text == test_case_payload["input_text"],
                )
            )
            if existing_test_case is None:
                db.add(TestCase(dataset_id=dataset.id, **test_case_payload))

        prompt_version_payload = payload["prompt_version"]
        prompt_version = db.scalar(
            select(PromptVersion).where(
                PromptVersion.name == prompt_version_payload["name"],
                PromptVersion.version == prompt_version_payload["version"],
            )
        )
        if prompt_version is None:
            prompt_version = PromptVersion(**prompt_version_payload)
            db.add(prompt_version)
            db.flush()

        experiment_payload = payload["experiment"]
        existing_experiment = db.scalar(
            select(Experiment).where(
                Experiment.name == experiment_payload["name"],
                Experiment.dataset_id == dataset.id,
                Experiment.prompt_version_id == prompt_version.id,
            )
        )
        if existing_experiment is None:
            db.add(
                Experiment(
                    dataset_id=dataset.id,
                    prompt_version_id=prompt_version.id,
                    **experiment_payload,
                )
            )

        db.commit()
        print("Sample data seeded successfully.")


if __name__ == "__main__":
    main()
