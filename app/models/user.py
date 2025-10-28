from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from .base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password_hash = Column(String)
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())