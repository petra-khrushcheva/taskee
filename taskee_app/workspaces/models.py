from sqlalchemy.orm import Mapped, mapped_column, relationship

from basemodels import Base


class Workspace(Base):
    name: Mapped[str]