from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    yolo_model_path: str = "yolov8n-face.pt"
    office_start: str = "09:00"
    office_end: str = "18:00"
    embedding_dir: str = "uploads/embeddings"  
    image_dir: str = "uploads/users"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()