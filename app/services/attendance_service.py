from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.attendance import Attendance
from app.models.session import Session
from app.services.session_manager import get_today_session_date

def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC

async def get_or_create_today_session(db: AsyncSession):
    """FIXED: Atomic get-or-create with unique constraint handling."""
    session_date = get_today_session_date()
    
    # First try to find existing
    result = await db.execute(
        select(Session).where(Session.session_date == session_date)
    )
    session = result.scalar_one_or_none()
    
    if session:
        return session
    
    # Create if not exists (race condition safe due to unique constraint)
    session = Session(session_date=session_date)
    db.add(session)
    
    try:
        await db.commit()
        await db.refresh(session)
    except Exception:
        await db.rollback()
        # Retry query - another transaction may have created it
        result = await db.execute(
            select(Session).where(Session.session_date == session_date)
        )
        session = result.scalar_one()
    
    return session

async def mark_attendance(db: AsyncSession, user_id: int, status: str = "present"):
    session = await get_or_create_today_session(db)

    result = await db.execute(
        select(Attendance).where(
            and_(
                Attendance.user_id == user_id,
                Attendance.session_id == session.id
            )
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