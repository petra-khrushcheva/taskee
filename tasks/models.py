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


class Task(TaskBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    time_created: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    pass

    # time_created = Column(TIMESTAMP, default=datetime.utcnow)

    # status = Column(Enum(TaskStatus), default=TaskStatus.new)
    # deadline = Column(DateTime)
    # workspace
    # created_by = Column(UUID, ForeignKey(user.uuid))
    # updated_at = Column(DateTime, default=datetime.datetime.utcnow,
    # server_default=text('now()', onupdate=datetime.datetime.now)
    # ispolnitel_id = Column(UUID, ForeignKey("users.uuid"))

    # ispolnitel = relationship("User", back_populates="tasks")












# from typing import Optional
# from datetime import datetime
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func


# class Role(Enum):
#     boss = 'boss'
#     not_a_boss = 'not_a_boss'


# from datetime import date, datetime
# from typing import Union, Optional
# from enum import Enum
# from uuid import UUID, uuid4

# from pydantic import BaseModel, EmailStr


# # class Role(str, Enum):
# #     boss = 'boss'
# #     not_a_boss = 'not_a_boss'
