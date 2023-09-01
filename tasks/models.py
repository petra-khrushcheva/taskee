from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field


class TaskStatus(str, Enum):
    new = 'new'
    wip = 'wip'
    done = 'done'


class TaskBase(SQLModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.new


class Task(TaskBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    time_created: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    pass
