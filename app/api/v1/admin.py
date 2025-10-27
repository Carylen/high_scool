from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from uuid import UUID
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.post("/assignments", response_model=schemas.AssignmentOut)
def create_assignment(
    assignment: schemas.AssignmentCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admin can create assignments")
    db_assignment = models.Assignment(
        title=assignment.title,
        description=assignment.description,
        due_date=assignment.due_date,
        created_by=current_user.id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/submissions/{submission_id}/grade")
def grade_submission(
    submission_id: UUID,
    grade: int = Body(..., ge=0, le=100),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admin can grade")
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(404, "Submission not found")
    submission.grade = grade
    submission.graded_by = current_user.id
    db.commit()
    return {"msg": "Graded successfully"}

@router.get("/attendances/pending")
def get_unverified_attendances(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Access denied")
    attendances = db.query(models.Attendance).filter(models.Attendance.verified == False).all()
    return attendances