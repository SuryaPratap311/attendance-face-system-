from datetime import datetime, timezone   # ← add timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.attendance import Attendance
from app.models.session import Session
from app.services.session_manager import get_today_session_date

def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)  # store as naive UTC

async def get_or_create_today_session(db: AsyncSession):
    session_date = get_today_session_date()
    result = await db.execute(select(Session).where(Session.session_date == session_date))
    session = result.scalar_one_or_none()

    if session:
        return session

    session = Session(session_date=session_date, start_time=_now(), status="open")
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def mark_attendance(db: AsyncSession, user_id: int, status: str = "present"):
    session = await get_or_create_today_session(db)

    result = await db.execute(
        select(Attendance).where(
            Attendance.user_id == user_id,
            Attendance.session_id == session.id
        )
    )
    attendance = result.scalar_one_or_none()

    if attendance:
        if attendance.check_out_time is None:
            attendance.check_out_time = _now()
            attendance.status = "checked_out"
            await db.commit()
            await db.refresh(attendance)
        return attendance

    attendance = Attendance(
        user_id=user_id,
        session_id=session.id,
        check_in_time=_now(),
        status=status,
    )
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance