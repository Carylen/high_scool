# app/schemas/__init__.py
from .auth import Token
from .user import UserLogin, UserCreate, UserOut
from .attendance import AttendanceCreate, AttendanceOut
from .assignment import AssignmentCreate, AssignmentOut
from .submission import SubmissionCreate, SubmissionOut

# Opsional: ekspor semua untuk kemudahan import
__all__ = [
    # Auth
    "Token",
    # User
    "UserLogin",
    "UserCreate",
    "UserOut",
    # Attendance
    "AttendanceCreate",
    "AttendanceOut",
    # Assignment
    "AssignmentCreate",
    "AssignmentOut",
    # Submission
    "SubmissionCreate",
    "SubmissionOut",
]