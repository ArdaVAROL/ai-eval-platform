from pydantic import BaseModel, Field, field_validator

from app.schemas.base import TimestampedSchema


class TestCaseCreate(BaseModel):
    dataset_id: int = Field(gt=0)
    input_text: str = Field(min_length=1)
    expected_output: str | None = None
    evaluation_type: str = Field(default="pass_fail", min_length=3, max_length=50)

    @field_validator("input_text", "expected_output", "evaluation_type")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        return cleaned or None

    @field_validator("input_text", "evaluation_type")
    @classmethod
    def require_non_empty_text(cls, value: str | None) -> str | None:
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class TestCaseRead(TimestampedSchema):
    dataset_id: int
    input_text: str
    expected_output: str | None = None
    evaluation_type: str
