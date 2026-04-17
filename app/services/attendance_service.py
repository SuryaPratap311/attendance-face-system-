from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.attendance import Attendance
from app.models.user import User


async def mark_attendance(db: AsyncSession, employee_id: str, status: str = "present") -> Attendance:
    result = await db.execute(
        select(User).where(User.employee_id == employee_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise ValueError(f"User {employee_id} not found")

    att = Attendance(
        employee_id=employee_id,
        timestamp=datetime.utcnow(),
        status=status,
    )
    db.add(att)
    await db.commit()
    await db.refresh(att)
    return att