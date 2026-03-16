from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import experiment as experiment_crud
from app.schemas.experiment import ExperimentCreate, ExperimentRead
from app.schemas.experiment_run import ExperimentRunBatchResponse

router = APIRouter()


@router.post("/", response_model=ExperimentRead, status_code=status.HTTP_201_CREATED)
def create_experiment(
    payload: ExperimentCreate,
    db: Session = Depends(get_db),
) -> ExperimentRead:
    return experiment_crud.create(db, payload)


@router.get("/", response_model=list[ExperimentRead])
def list_experiments(db: Session = Depends(get_db)) -> list[ExperimentRead]:
    return experiment_crud.list_all(db)


@router.post(
    "/{experiment_id}/run",
    response_model=ExperimentRunBatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def trigger_experiment_run(experiment_id: int, db: Session = Depends(get_db)) -> ExperimentRunBatchResponse:
    runs = experiment_crud.run_experiment(db, experiment_id)
    if runs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    return ExperimentRunBatchResponse(experiment_id=experiment_id, created_runs=len(runs), runs=runs)
