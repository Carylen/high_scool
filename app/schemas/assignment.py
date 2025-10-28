from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: datetime

class AssignmentOut(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: datetime

    class Config:
        from_attributes = True