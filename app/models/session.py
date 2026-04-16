# app/models/session.py - Replace  
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func 
from app.models.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_date: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())  
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")