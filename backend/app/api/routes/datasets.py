from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import dataset as dataset_crud
from app.schemas.dataset import DatasetCreate, DatasetRead

router = APIRouter()


@router.post("/", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
def create_dataset(payload: DatasetCreate, db: Session = Depends(get_db)) -> DatasetRead:
    return dataset_crud.create(db, payload)


@router.get("/", response_model=list[DatasetRead])
def list_datasets(db: Session = Depends(get_db)) -> list[DatasetRead]:
    return dataset_crud.list_all(db)
