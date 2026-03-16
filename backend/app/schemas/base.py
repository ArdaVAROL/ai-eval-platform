from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampedSchema(ORMBaseModel):
    id: int
    created_at: datetime
