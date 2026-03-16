from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.dataset import Dataset
from app.models.test_case import TestCase
from app.schemas.test_case import TestCaseCreate


def create(db: Session, payload: TestCaseCreate) -> TestCase:
    dataset = db.get(Dataset, payload.dataset_id)
    if dataset is None:
        raise AppError(status.HTTP_404_NOT_FOUND, "Dataset not found.")

    test_case = TestCase(**payload.model_dump())
    db.add(test_case)
    db.commit()
    db.refresh(test_case)
    return test_case


def list_all(db: Session) -> list[TestCase]:
    return list(db.scalars(select(TestCase).order_by(TestCase.created_at.desc())).all())
