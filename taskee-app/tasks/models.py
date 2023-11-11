import enum

from basemodels import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column


class TaskStatus(enum.Enum):
    new = 'new'
    wip = 'wip'
    completed = 'completed'


class Task(Base):
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus]
    # deadline
    # creator: Mapped[User]
    # appointed_to: Mapped[User | None]
