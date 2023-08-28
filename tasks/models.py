from typing import Optional
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field




class TaskBase(SQLModel):
    title: str
    description: str


class Task(TaskBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)


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

























# from datetime import datetime
# from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, Integer, String, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from enum import Enum




    # time_created = Column(TIMESTAMP, default=datetime.utcnow)

    # status = Column(Enum(TaskStatus), default=TaskStatus.new)
    # deadline = Column(DateTime)
    # workspace
    # created_by = Column(UUID, ForeignKey(user.uuid))
    # updated_at = Column(DateTime, default=datetime.datetime.utcnow,
    # server_default=text('now()', onupdate=datetime.datetime.now)
    # ispolnitel_id = Column(UUID, ForeignKey("users.uuid"))

    # ispolnitel = relationship("User", back_populates="tasks")


# class TaskStatus(Enum):
#     new = 'new'
#     wip = 'WIP'
#     done = 'done'


# class Role(Enum):
#     boss = 'boss'
#     not_a_boss = 'not_a_boss'





# class UserModel(Base):
#     __tablename__ = "users"

#     uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # username = Column(String, unique=True)
#     email = Column(String)
#     first_name = Column(String)
#     last_name = Column(String)
#     role = Column(Enum(Role), default=TaskStatus.not_a_boss)
#     tasks = relationship("Task", back_populates="ispolnitel")
#     workspaces = relationship("Workspace", back_populates="participant")

# from datetime import date, datetime
# from typing import Union, Optional
# from enum import Enum
# from uuid import UUID, uuid4

# from pydantic import BaseModel, EmailStr


# # описывает, что позволено отправлять в наш api
# class TaskBaseSchema(BaseModel):
#     title: str
#     description: Union[str, None] = None
#     # status: TaskStatus
#     #deadline: Union[date, None] = None #ограничение, не раньше даты создания
#     # workspace
#     # created_by
#     # assigned to


# class TaskCreateSchema(TaskBaseSchema):
#     pass


# class TaskSchema(TaskBaseSchema):
#     uuid: Optional[UUID] = uuid4
#     # time_created: datetime

#     class Config:
#         orm_mode = True


# # class TaskStatus(str, Enum):
# #     new = 'new'
# #     wip = 'WIP'
# #     done = 'done'


# # class Role(str, Enum):
# #     boss = 'boss'
# #     not_a_boss = 'not_a_boss'


# # class User(BaseModel):
# #     id: Optional[UUID] = uuid4()
# #     username: str
# #     first_name: Union[str, None] = None
# #     last_name: Union[str, None] = None
# #     role: Union[Role, None] = None
# #     email: EmailStr
