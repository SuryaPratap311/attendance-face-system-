from datetime import date, datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attendance import Attendance
from app.models.session import Session

async def get_or_create_today_session(db: AsyncSession):
    """No race condition — simple approach."""
    today_date = date.today()
    
    # 1. Try to find
    result = await db.execute(
        select(Session.id).where(Session.session_date == today_date)
    )
    session_id = result.scalar()
    
    if session_id:
        # 2. Load full session
        result = await db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one()
    
    # 3. Create new (no race condition risk)
    session = Session(session_date=today_date)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def mark_attendance(db: AsyncSession, user_id: int, status: str = "present"):
    session = await get_or_create_today_session(db)

    # ✅ Check if already marked today
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
        # Already marked — update if checkout pending
        if attendance.check_out_time is None:
            attendance.check_out_time = datetime.now()
            attendance.status = "checked_out"
        else:
            return attendance  # Already complete
        
        await db.commit()
        await db.refresh(attendance)
        return attendance

    # New check-in
    attendance = Attendance(
        user_id=user_id,
        session_id=session.id,
        check_in_time=datetime.now(),
        status=status,
    )
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance