from datetime import datetime, date
from app.core.config import settings

def get_today_session_date() -> str:
    return date.today().isoformat()

def is_entry_time() -> bool:
    return datetime.now().strftime("%H:%M") <= settings.office_start

def is_exit_time() -> bool:
    return datetime.now().strftime("%H:%M") >= settings.office_end