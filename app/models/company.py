from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
# from models import UserViewModel


class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: bool
    rating: float
    # users: Optional[list[UserViewModel]] = None

    class Config:
        orm_mode = True


class CompanyCreateModel(BaseModel):
    name: str
    description: str
    mode: bool
    rating: float


class CompanyUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[bool] = None
    rating: Optional[float] = None
