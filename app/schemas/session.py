from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SessionCreate(BaseModel):
    session_date: str

class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_date: str
    start_time: datetime
    end_time: datetime | None = None
    status: str