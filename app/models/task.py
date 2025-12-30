from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(
            TaskStatus,
            name="taskstatus",
            create_type=False,
            values_callable=lambda enum: [e.value for e in enum]  
        ),
        default=TaskStatus.PENDING,
        nullable=False,
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
