import enum
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.basemodels import Base


class TaskStatus(enum.Enum):
    new = "new"
    wip = "wip"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        server_default=TaskStatus.new.value
    )
    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    executor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        )
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE")
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_tasks", foreign_keys=[creator_id]
    )
    executor: Mapped["User"] = relationship(
        back_populates="appointed_tasks", foreign_keys=[executor_id]
    )
    workspace: Mapped["Workspace"] = relationship(back_populates="tasks")

    # deadline (default - in a month)
