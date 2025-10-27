from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.models import models
from app.database.db import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/api/v1/parent", tags=["parent"])

@router.get("/children/{child_id}/attendances")
def get_child_attendances(
    child_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "parent":
        raise HTTPException(403, "Access denied")
    student = db.query(models.Student).filter(
        models.Student.id == child_id,
        models.Student.parent_id == current_user.id
    ).first()
    if not student:
        raise HTTPException(404, "Child not found or not yours")
    attendances = db.query(models.Attendance).filter(models.Attendance.student_id == child_id).all()
    return attendances

@router.get("/children/{child_id}/grades")
def get_child_grades(
    child_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "parent":
        raise HTTPException(403, "Access denied")
    student = db.query(models.Student).filter(
        models.Student.id == child_id,
        models.Student.parent_id == current_user.id
    ).first()
    if not student:
        raise HTTPException(404, "Child not found")
    submissions = db.query(models.Submission).filter(models.Submission.student_id == child_id).all()
    return [{"assignment_id": s.assignment_id, "grade": s.grade} for s in submissions]