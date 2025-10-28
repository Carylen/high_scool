from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from app import models
from app.database import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/api/v1/student", tags=["student"])

@router.post("/attendance")
async def record_attendance(
    lat: float = Body(..., ge=-90, le=90),
    lon: float = Body(..., ge=-180, le=180),
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "student":
        raise HTTPException(403, "Only students can attend")
    result = await db.execute(select(models.Student).where(models.Student.user_id == current_user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(404, "Student profile not found")
    today = date.today()
    existing = await db.execute(
        select(models.Attendance)
        .where(models.Attendance.student_id == student.id)
        .where(models.Attendance.date == today)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Already attended today")
    new_att = models.Attendance(student_id=student.id, latitude=lat, longitude=lon)
    db.add(new_att)
    await db.commit()
    await db.refresh(new_att)
    return {"status": "Attendance recorded", "id": new_att.id}

@router.post("/submissions")
async def submit_assignment(
    assignment_id: str = Body(...),
    file_url: str = Body(None),
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "student":
        raise HTTPException(403, "Only students can submit")
    result = await db.execute(select(models.Student).where(models.Student.user_id == current_user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(404, "Student not found")
    db_sub = models.Submission(assignment_id=assignment_id, student_id=student.id, file_url=file_url)
    db.add(db_sub)
    await db.commit()
    return {"msg": "Submitted"}