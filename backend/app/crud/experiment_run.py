from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experiment_run import ExperimentRun


def list_all(db: Session) -> list[ExperimentRun]:
    return list(db.scalars(select(ExperimentRun).order_by(ExperimentRun.created_at.desc())).all())
