from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="YOLO Attendance POC")
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}