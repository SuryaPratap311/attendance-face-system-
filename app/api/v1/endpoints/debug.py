from fastapi import APIRouter
from app.services.demo_orchestrator import start_poc

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/start")
def start_demo():
    start_poc()
    return {"status": "started"}