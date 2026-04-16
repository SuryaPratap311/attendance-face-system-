from fastapi import APIRouter
from app.api.v1.endpoints import attendance, user, debug  

api_router = APIRouter()
api_router.include_router(attendance.router)
api_router.include_router(user.router)  
api_router.include_router(debug.router)