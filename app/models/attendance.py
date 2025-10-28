from sqlalchemy import Column, Float, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from uuid import uuid4
from .base import Base

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    date = Column(Date, default=date.today)
    latitude = Column(Float)
    longitude = Column(Float)
    verified = Column(Boolean, default=False)