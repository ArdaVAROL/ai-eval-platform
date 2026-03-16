from pydantic import BaseModel, Field, field_validator

from app.schemas.base import TimestampedSchema


class ExperimentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    dataset_id: int = Field(gt=0)
    prompt_version_id: int = Field(gt=0)
    model_name: str = Field(min_length=2, max_length=255)

    @field_validator("name", "model_name")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("This field cannot be empty.")
        return cleaned


class ExperimentRead(TimestampedSchema):
    name: str
    dataset_id: int
    prompt_version_id: int
    model_name: str
