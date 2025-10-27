from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from uuid import UUID
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/api/v1/student", tags=["student"])

@router.post("/attendance")
def record_attendance(
    lat: float = Body(...),
    lon: float = Body(...),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "student":
        raise HTTPException(403, "Only students can attend")
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "Student profile not found")
    from datetime import date
    existing = db.query(models.Attendance).filter(
        models.Attendance.student_id == student.id,
        models.Attendance.date == date.today()
    ).first()
    if existing:
        raise HTTPException(400, "Already attended today")
    new_att = models.Attendance(student_id=student.id, latitude=lat, longitude=lon)
    db.add(new_att)
    db.commit()
    return {"status": "Attendance recorded"}

@router.post("/submissions")
def submit_assignment(
    submission: schemas.SubmissionCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "student":
        raise HTTPException(403, "Only students can submit")
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db_sub = models.Submission(
        assignment_id=submission.assignment_id,
        student_id=student.id,
        file_url=submission.file_url
    )
    db.add(db_sub)
    db.commit()
    return {"msg": "Submitted"}