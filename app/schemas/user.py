from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    role: str
    department: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str
    name: str
    role: str
    department: str
    image_path: str | None = None
    embedding_path: str | None = None
    status: str