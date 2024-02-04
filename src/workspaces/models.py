import enum
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.basemodels import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(String(50))

    users: Mapped[list['WorkspaceUserAssociation']] = relationship(
        back_populates='workspace'
    )
    tasks: Mapped[list['Task']] = relationship(back_populates='workspace')
    # tasks_new: Mapped[list['Task']] = relationship(
    #     back_populates='workspace',
    #     primaryjoin='and_(Workspace.id == Task.workspace_id, Task.status == "new")',
    #     order_by='Task.created_at.desc()'
    #     )
    # для примера как создавать ограничение на уровне relationship


class GroupRole(enum.Enum):
    admin = 'admin'
    user = 'user'
    reader = 'reader'


class WorkspaceUserAssociation(Base):
    __tablename__ = "workspace_user_association"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "workspace_id",
            name="unique_workspace_user",
        ),
    )

    workspace_id: Mapped[UUID] = mapped_column(
        ForeignKey('workspaces.id', ondelete='CASCADE'),
        nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    role: Mapped[GroupRole]

    workspace: Mapped["Workspace"] = relationship(
        back_populates="users",
    )

    user: Mapped["User"] = relationship(
        back_populates="workspaces",
    )
