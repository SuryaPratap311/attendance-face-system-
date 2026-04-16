# app/services/session_manager.py - Replace entire file
from datetime import datetime, date, time, timezone
from app.core.config import settings

def get_today_session_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()

def parse_time(time_str: str) -> time:
    """Parse 'HH:MM' string to time object."""
    return datetime.strptime(time_str, "%H:%M").time()

def is_entry_time() -> bool:
    """Check if current time is during office entry window."""
    now = datetime.now().time()
    office_start = parse_time(settings.office_start)
    office_end = parse_time(settings.office_end)
    return office_start <= now <= office_end  # ← FIXED logic

def is_exit_time() -> bool:
    """Check if current time is during office exit window."""
    now = datetime.now().time()
    office_end = parse_time(settings.office_end)
    return now >= office_end  # ← FIXED logic