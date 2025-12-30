from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional
from math import ceil


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    
    tasks = db.query(Task).order_by(Task.created_at.desc()).offset(skip).limit(page_size).all()
    total = db.query(func.count(Task.id)).scalar()
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True