from typing import List
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from schemas import Task, TaskStatus, User
from models import TaskViewModel, TaskCreateModel, TaskUpdateModel
from schemas.user import get_password_hash
router = APIRouter(prefix="/tasks", tags=["Task"])


@router.get("")
async def get_tasks(db: Session = Depends(get_db_context)) -> List[TaskViewModel]:
    return db.query(Task).filter(Task.status != TaskStatus.CLOSED).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskCreateModel, db: Session = Depends(get_db_context)) -> None:
    task = Task(**request.dict())
    user = db.query(User).filter(User.id == request.user_id).first()
    if user is None:
        raise HTTPException(status_code=422, detail="Invalid User ID")
    task.summary = request.summary
    task.description = request.description
    task.status = request.status
    task.priority = request.priority
    task.created_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()


@router.put("/{company_id}")
async def update_task(task_id: UUID, request: TaskUpdateModel, db: Session = Depends(get_db_context)) -> TaskViewModel:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if request.user_id is not None:
        task.user_id = request.user_id
    if request.summary is not None:
        task.summary = request.summary
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status
    if request.priority is not None:
        task.priority = request.priority
    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
