from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import test_case as test_case_crud
from app.schemas.test_case import TestCaseCreate, TestCaseRead

router = APIRouter()


@router.post("/", response_model=TestCaseRead, status_code=status.HTTP_201_CREATED)
def create_test_case(payload: TestCaseCreate, db: Session = Depends(get_db)) -> TestCaseRead:
    return test_case_crud.create(db, payload)


@router.get("/", response_model=list[TestCaseRead])
def list_test_cases(db: Session = Depends(get_db)) -> list[TestCaseRead]:
    return test_case_crud.list_all(db)
