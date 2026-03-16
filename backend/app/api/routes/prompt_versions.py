from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import prompt_version as prompt_version_crud
from app.schemas.prompt_version import PromptVersionCreate, PromptVersionRead

router = APIRouter()


@router.post("/", response_model=PromptVersionRead, status_code=status.HTTP_201_CREATED)
def create_prompt_version(
    payload: PromptVersionCreate,
    db: Session = Depends(get_db),
) -> PromptVersionRead:
    return prompt_version_crud.create(db, payload)


@router.get("/", response_model=list[PromptVersionRead])
def list_prompt_versions(db: Session = Depends(get_db)) -> list[PromptVersionRead]:
    return prompt_version_crud.list_all(db)
