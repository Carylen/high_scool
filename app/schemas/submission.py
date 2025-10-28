from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SubmissionCreate(BaseModel):
    assignment_id: UUID
    file_url: Optional[str] = None

class SubmissionOut(BaseModel):
    id: UUID
    assignment_id: UUID
    grade: Optional[int]

    class Config:
        from_attributes = True