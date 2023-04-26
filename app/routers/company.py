from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from services.auth import token_interceptor
from database import get_db_context

from schemas import Company, User
from models import CompanyCreateModel, CompanyViewModel, CompanyUpdateModel

router = APIRouter(prefix="/companies", tags=["Company"])


@router.get("", response_model=List[CompanyViewModel])
async def get_all_companies(
        name: str = Query(default=None),
        mode: bool = Query(default=None),
        page: int = Query(ge=1, default=1),
        size: int = Query(ge=1, le=50, default=10),
        user: User = Depends(token_interceptor),
        db: Session = Depends(get_db_context)
) -> List[CompanyViewModel]:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied")

    # Default of joinedload is LEFT OUTER JOIN
    query = db.query(Company)

    if name is not None:
        query = query.filter(Company.name.like(f"{name}%"))
    if mode is not None:
        query = query.filter(Company.mode == mode)

    return query.offset((page-1)*size).limit(size).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyCreateModel, db: Session = Depends(get_db_context)) -> None:
    company = Company(**request.dict())
    company.created_at = datetime.utcnow()
    company.updated_at = datetime.utcnow()

    db.add(company)
    db.commit()


@router.get("/{company_id}")
async def get_Company_detail(company_id: UUID, db: Session = Depends(get_db_context)) -> CompanyViewModel:
    return db.query(Company).filter(Company.id == company_id)\
        .first()


@router.put("/{company_id}")
async def update_company(company_id: UUID, request: CompanyUpdateModel, db: Session = Depends(get_db_context)) -> CompanyViewModel:
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if request.name is not None:
        company.name = request.name
    if request.description is not None:
        company.description = request.description
    if request.mode is not None:
        company.mode = request.mode
    if request.rating is not None:
        company.rating = request.rating
    company.updated_at = datetime.utcnow()
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
