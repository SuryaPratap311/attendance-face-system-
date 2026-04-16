from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    yolo_model_path: str = "yolov8n.pt"
    office_start: str = "09:00"
    office_end: str = "18:00"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()