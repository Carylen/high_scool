from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

class AttendanceCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

class AttendanceOut(BaseModel):
    id: UUID
    date: date
    latitude: float
    longitude: float
    verified: bool

    class Config:
        from_attributes = True