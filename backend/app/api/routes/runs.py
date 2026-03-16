from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import experiment_run as experiment_run_crud
from app.schemas.experiment_run import ExperimentRunRead

router = APIRouter()


@router.get("/", response_model=list[ExperimentRunRead])
def list_runs(db: Session = Depends(get_db)) -> list[ExperimentRunRead]:
    return experiment_run_crud.list_all(db)
