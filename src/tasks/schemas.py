from datetime import datetime
from typing import Annotated
from uuid import UUID

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict

from tasks.models import TaskStatus
from users.schemas import UserRead


class TaskBase(BaseModel):
    title: Annotated[str, MaxLen(50)]
    description: str
    status: TaskStatus = TaskStatus.new
    # deadline


class TaskCreate(TaskBase):
    creator_id: UUID  # а нафига его передавать, если он автоматически добавится из get current user?
    executor_id: UUID | None = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    creator: UserRead
    # creator: "UserRead" теоретически это должно работать без импорта, я хз как но надо проверить
    executor: UserRead | None = None
