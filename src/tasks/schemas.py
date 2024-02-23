from typing import Annotated
from uuid import UUID

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict

from tasks.models import TaskStatus
from users.schemas import UserRead


class TaskBase(BaseModel):
    title: Annotated[str, MaxLen(50)]
    description: str | None = None
    status: TaskStatus = TaskStatus.new.value
# возможно в придется убрать str из самого энума, если алхимия будет ругаться
    # deadline


class TaskCreate(TaskBase):
    executor_id: UUID | None = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class TaskWithExecutor(TaskRead):
    executor: UserRead | None = None
