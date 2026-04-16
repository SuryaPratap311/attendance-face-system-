from fastapi import APIRouter
from app.services.camera_worker import run_camera_loop
import asyncio

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/start")
async def start_demo():
    asyncio.create_task(asyncio.to_thread(run_camera_loop))  
    return {"status": "started"}