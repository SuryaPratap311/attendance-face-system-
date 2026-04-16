from fastapi import APIRouter
from app.api.v1.endpoints import attendance, user  # ← user add

api_router = APIRouter()
api_router.include_router(attendance.router)
api_router.include_router(user.router)  