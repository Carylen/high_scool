from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date

# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str  # 'admin', 'student', 'parent'

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str

# --- Attendance ---
class AttendanceCreate(BaseModel):
    latitude: float
    longitude: float

class AttendanceOut(BaseModel):
    id: UUID
    date: date
    latitude: float
    longitude: float
    verified: bool

# --- Assignment ---
class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: datetime

class AssignmentOut(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: datetime

# --- Submission ---
class SubmissionCreate(BaseModel):
    assignment_id: UUID
    file_url: Optional[str] = None

class SubmissionOut(BaseModel):
    id: UUID
    assignment_id: UUID
    grade: Optional[int]