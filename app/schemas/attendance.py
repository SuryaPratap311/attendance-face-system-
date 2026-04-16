from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AttendanceCreate(BaseModel):
    user_id: int
    session_id: int
    status: str = "present"

class AttendanceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    session_id: int
    check_in_time: datetime
    check_out_time: datetime | None = None
    status: str