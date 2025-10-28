from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app import models
from app.database import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/api/v1/parent", tags=["parent"])

@router.get("/children/{child_id}/attendances")
async def get_child_attendances(
    child_id: UUID,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "parent":
        raise HTTPException(403, "Access denied")
    result = await db.execute(
        select(models.Student)
        .where(models.Student.id == child_id)
        .where(models.Student.parent_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(404, "Child not found or not yours")
    attendances = await db.execute(select(models.Attendance).where(models.Attendance.student_id == child_id))
    return attendances.scalars().all()

@router.get("/children/{child_id}/grades")
async def get_child_grades(
    child_id: UUID,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "parent":
        raise HTTPException(403, "Access denied")
    result = await db.execute(
        select(models.Student)
        .where(models.Student.id == child_id)
        .where(models.Student.parent_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(404, "Child not found")
    submissions = await db.execute(select(models.Submission).where(models.Submission.student_id == child_id))
    return [{"assignment_id": s.assignment_id, "grade": s.grade} for s in submissions.scalars()]