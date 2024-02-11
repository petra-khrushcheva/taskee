from uuid import UUID

from pydantic import BaseModel, ConfigDict

# TYPE_CHEKING ????

class WorkspaceBase(BaseModel):
    name: str
    description: str | None = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class WorkspaceWithTasks(WorkspaceRead):
    # tasks: list[Task] ????
    pass


class MembershipCreate(BaseModel):
    pass
