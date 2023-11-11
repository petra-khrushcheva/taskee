from annotated_types import MaxLen
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel

from tasks.models import TaskStatus


class TaskBase(BaseModel):
    title: Annotated[str, MaxLen(50)]
    description: str
    status: TaskStatus = TaskStatus.new
    # deadline
    # creator
    # appointed_to


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
