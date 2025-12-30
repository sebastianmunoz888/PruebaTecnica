from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    items: list[Task]
    total: int
    page: int
    page_size: int
    total_pages: int