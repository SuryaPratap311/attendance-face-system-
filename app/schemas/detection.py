from pydantic import BaseModel, ConfigDict

class DetectionResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int | None = None
    name: str | None = None
    confidence: float | None = None
    detected: bool = False