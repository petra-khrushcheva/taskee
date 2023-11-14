from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from annotated_types import MaxLen
from pydantic import BaseModel
from users.schemas import UserRead
from tasks.models import TaskStatus


class TaskBase(BaseModel):
    title: Annotated[str, MaxLen(50)]
    description: str
    status: TaskStatus = TaskStatus.new
    # deadline


class TaskCreate(TaskBase):
    creator_id: UUID
    executor_id: Optional[UUID] = None


class Task(TaskBase):
    id: UUID
    created_at: datetime
    creator: UserRead
    executor: Optional[UserRead]

    class Config:
        from_attributes = True
