from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.basemodels import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    created_tasks: Mapped[list['Task']] = relationship(
        back_populates='creator',
        foreign_keys='Task.creator_id'
    )
    appointed_tasks: Mapped[list['Task']] = relationship(
        back_populates='executor',
        foreign_keys='Task.executor_id'
    )

    workspaces: Mapped[list['WorkspaceUserAssociation']] = relationship(
        back_populates='user'
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
