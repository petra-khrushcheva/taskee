from uuid import UUID

from pydantic import BaseModel, ConfigDict

from workspaces.models import GroupRole
from users.schemas import UserRead
from tasks.schemas import TaskRead


class WorkspaceBase(BaseModel):
    name: str
    description: str | None = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class WorkspaceWithTasks(WorkspaceRead):
    tasks: list[TaskRead]


class MembershipCreate(BaseModel):
    user_id: UUID
    user_role: GroupRole = GroupRole.user
# возможно value,
# возможно в придется убрать str из самого энума, если алхимия будет ругаться


class WorkspaceUser(UserRead):
    role_in_ws: GroupRole


class UserWithTasks(WorkspaceUser):
    tasks: list[TaskRead]
