from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import metrics as metrics_crud
from app.schemas.metrics import MetricsSummaryRead

router = APIRouter()


@router.get("/summary", response_model=MetricsSummaryRead)
def get_summary_metrics(db: Session = Depends(get_db)) -> MetricsSummaryRead:
    return metrics_crud.get_summary(db)
