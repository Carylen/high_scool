from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app import models, schemas
from app.database.db import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.post("/assignments", response_model=schemas.AssignmentOut)
async def create_assignment(
    assignment: schemas.AssignmentCreate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
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
    await db.commit()
    await db.refresh(db_assignment)
    return db_assignment

@router.put("/submissions/{submission_id}/grade")
async def grade_submission(
    submission_id: UUID,
    grade: int = Body(..., ge=0, le=100),
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admin can grade")
    result = await db.execute(select(models.Submission).where(models.Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(404, "Submission not found")
    submission.grade = grade
    submission.graded_by = current_user.id
    await db.commit()
    return {"msg": "Graded successfully"}

@router.get("/attendances/pending")
async def get_unverified_attendances(
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Access denied")
    result = await db.execute(select(models.Attendance).where(models.Attendance.verified == False))
    return result.scalars().all()