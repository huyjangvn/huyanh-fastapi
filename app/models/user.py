from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
# from models import CompanyViewModel, TaskViewModel


class UserViewModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    company_id: Optional[str] = None
    # company: Optional[CompanyViewModel] = None
    # tasks: Optional[list[TaskViewModel]] = None

    class Config:
        orm_mode = True


class UserCreateModel(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    company_id: Optional[str] = None
    password: str


class UserUpdateModel(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    company_id: Optional[str] = None
    password: Optional[str] = None
