from pydantic import BaseModel, Field, field_validator

from app.schemas.base import TimestampedSchema


class PromptVersionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    version: str = Field(min_length=1, max_length=50)
    prompt_text: str = Field(min_length=1)

    @field_validator("name", "version", "prompt_text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("This field cannot be empty.")
        return cleaned


class PromptVersionRead(TimestampedSchema):
    name: str
    version: str
    prompt_text: str
