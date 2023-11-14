from typing import List
from basemodels import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    created_tasks: Mapped[List["Task"]] = relationship(
        back_populates="creator"
    )
    appointed_tasks: Mapped[List["Task"]] = relationship(
        back_populates="executor"
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
