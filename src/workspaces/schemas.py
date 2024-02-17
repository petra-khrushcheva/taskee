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


class WorkspaceUpdate(WorkspaceBase):
    name: str | None = None


class WorkspaceRead(WorkspaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class WorkspaceWithTasks(WorkspaceRead):
    tasks: list[TaskRead]


class MembershipUpdate(BaseModel):
    user_role: GroupRole = GroupRole.user.value
# возможно в придется убрать str из самого энума, если алхимия будет ругаться


class MembershipCreate(MembershipUpdate):
    user_id: UUID


class WorkspaceUser(UserRead):
    role_in_ws: GroupRole


class UserWithTasks(WorkspaceUser):
    tasks: list[TaskRead]
