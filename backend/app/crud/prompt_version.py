from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.prompt_version import PromptVersion
from app.schemas.prompt_version import PromptVersionCreate


def create(db: Session, payload: PromptVersionCreate) -> PromptVersion:
    existing_prompt_version = db.scalar(
        select(PromptVersion).where(
            PromptVersion.name == payload.name,
            PromptVersion.version == payload.version,
        )
    )
    if existing_prompt_version is not None:
        raise AppError(status.HTTP_409_CONFLICT, "This prompt version already exists.")

    prompt_version = PromptVersion(**payload.model_dump())
    db.add(prompt_version)
    db.commit()
    db.refresh(prompt_version)
    return prompt_version


def list_all(db: Session) -> list[PromptVersion]:
    return list(db.scalars(select(PromptVersion).order_by(PromptVersion.created_at.desc())).all())
