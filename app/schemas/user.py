from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    employee_id: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    employee_id: str
    embedding_path: str | None = None
    image_path: str | None = None