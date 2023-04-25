from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
# from models import UserViewModel


class TaskViewModel(BaseModel):
    id: UUID
    user_id: str
    summary: str
    description: str
    status: str
    priority: int
    # user: Optional[UserViewModel] = None

    class Config:
        orm_mode = True


class TaskCreateModel(BaseModel):
    user_id: UUID
    summary: str
    description: str
    status: str
    priority: int


class TaskUpdateModel(BaseModel):
    user_id: Optional[UUID] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
