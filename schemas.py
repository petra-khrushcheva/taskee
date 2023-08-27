from datetime import date
from typing import Union, Optional
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr


# описывает, что позволено отправлять в наш api
class TaskBaseSchema(BaseModel):
    title: str
    description: Union[str, None] = None
    # status: TaskStatus
    # deadline:  Union[date, None] = None #ограничение, не раньше даты создания
    # workspace
    # created_by
    # assigned to


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskSchema(TaskBaseSchema):
    uuid: Optional[UUID] = uuid4
    # time_created: date

    class Config:
        orm_mode = True


# class TaskStatus(str, Enum):
#     new = 'new'
#     wip = 'WIP'
#     done = 'done'


# class Role(str, Enum):
#     boss = 'boss'
#     not_a_boss = 'not_a_boss'


# class User(BaseModel):
#     id: Optional[UUID] = uuid4()
#     username: str
#     first_name: Union[str, None] = None
#     last_name: Union[str, None] = None
#     role: Union[Role, None] = None
#     email: EmailStr
