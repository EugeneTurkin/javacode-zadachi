from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from utils.database import Base


class TaskStatus(Enum):
    PENDING="pending"
    PROCESSING="processing"
    COMPLETED="completed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    task_name: Mapped[str] = mapped_column(String(200), nullable=False, unique=False)
    task_status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus, name="status_enum"), nullable=False)
    worder_id: Mapped[int] = mapped_column(Integer(), nullable=True)


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None, nullable=False)

    
