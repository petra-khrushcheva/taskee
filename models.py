from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from enum import Enum

from database import Base


# class TaskStatus(Enum):
#     new = 'new'
#     wip = 'WIP'
#     done = 'done'


# class Role(Enum):
#     boss = 'boss'
#     not_a_boss = 'not_a_boss'


class Task(Base):
    __tablename__ = "task"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String)
    description = Column(Text)
    # status = Column(Enum(TaskStatus), default=TaskStatus.new)
    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    # deadline = Column(DateTime)
    # workspace
    # created_by = Column(UUID, ForeignKey(user.uuid))
    # updated_at = Column(DateTime, default=datetime.datetime.now,
    # server_default=text('now()', onupdate=datetime.datetime.now)
    # ispolnitel_id = Column(UUID, ForeignKey("users.uuid"))

    # ispolnitel = relationship("User", back_populates="tasks")


# class UserModel(Base):
#     __tablename__ = "user"

#     uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # username = Column(String, unique=True)
#     email = Column(String)
#     first_name = Column(String)
#     last_name = Column(String)
#     role = Column(Enum(Role), default=TaskStatus.not_a_boss)
#     tasks = relationship("Task", back_populates="ispolnitel")
#     workspaces = relationship("Workspace", back_populates="participant")
