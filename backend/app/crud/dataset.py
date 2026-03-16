from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate


def create(db: Session, payload: DatasetCreate) -> Dataset:
    existing_dataset = db.scalar(select(Dataset).where(Dataset.name == payload.name))
    if existing_dataset is not None:
        raise AppError(status.HTTP_409_CONFLICT, "A dataset with this name already exists.")

    dataset = Dataset(**payload.model_dump())
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


def list_all(db: Session) -> list[Dataset]:
    return list(db.scalars(select(Dataset).order_by(Dataset.created_at.desc())).all())
