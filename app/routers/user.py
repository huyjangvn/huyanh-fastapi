from typing import List
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from schemas import User, Company
from models import UserViewModel, UserCreateModel, UserUpdateModel
from schemas.user import get_password_hash
from services.auth import token_interceptor
router = APIRouter(prefix="/users", tags=["User"])


@router.get("")
async def get_users(db: Session = Depends(get_db_context)) -> List[UserViewModel]:
    return db.query(User).filter(User.is_active == True).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreateModel, db: Session = Depends(get_db_context)) -> None:
    hashed_password = get_password_hash(request.password)
    del request.password
    user = User(**request.dict())
    if request.company_id is not None:
        company = db.query(Company).filter(
            Company.id == request.company_id).first()
        if company is None:
            raise HTTPException(status_code=422, detail="Invalid Company ID")
        user.company_id = request.company_id
    user.hashed_password = hashed_password
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()

    db.add(user)
    db.commit()


@router.put("/{user_id}")
async def update_user(user_id: UUID, request: UserUpdateModel, db: Session = Depends(get_db_context),
                      logged_in_user: User = Depends(token_interceptor)) -> UserViewModel:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # only allow non-admin user to update their own profile
    if logged_in_user.id != user.id and logged_in_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    if request.email is not None:
        user.email = request.email
    if request.username is not None:
        user.username = request.username
    if request.first_name is not None:
        user.first_name = request.first_name
    if request.last_name is not None:
        user.last_name = request.last_name
    if request.is_active is not None:
        user.is_active = request.is_active
    if request.is_admin is not None:  # todo: check if user is admin before updating
        if logged_in_user.is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")
        user.is_admin = request.is_admin
    if request.company_id is not None:  # todo: check if company exists
        company = db.query(Company).get(request.company_id)
        if company is None:
            raise HTTPException(status_code=422, detail="Invalid Company ID")
        user.company_id = request.company_id
    if request.password is not None:
        user.hashed_password = get_password_hash(request.password)
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
