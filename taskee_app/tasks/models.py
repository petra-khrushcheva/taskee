import enum
import uuid

from basemodels import Base
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TaskStatus(enum.Enum):
    new = 'new'
    wip = 'wip'
    completed = 'completed'


class Task(Base):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus]
    creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"),
                                                  nullable=False)
    executor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"),
                                                          nullable=False)

    creator: Mapped["User"] = relationship(back_populates='created_tasks')
    executor: Mapped["User"] = relationship(back_populates='appointed_tasks')

    # deadline
