from pydantic import BaseModel, Field, field_validator

from app.schemas.base import TimestampedSchema


class DatasetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("name", "description")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        return cleaned or None

    @field_validator("name")
    @classmethod
    def require_non_empty_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Name cannot be empty.")
        return value


class DatasetRead(TimestampedSchema):
    name: str
    description: str | None = None
