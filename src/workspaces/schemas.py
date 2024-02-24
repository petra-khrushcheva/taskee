from uuid import UUID

from pydantic import BaseModel, ConfigDict

from workspaces.models import GroupRole
from users.schemas import UserRead
from tasks.schemas import TaskWithExecutor, TaskRead


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
    tasks: list[TaskWithExecutor]


class MembershipUpdate(BaseModel):
    user_role: GroupRole = GroupRole.user.value


class MembershipCreate(MembershipUpdate):
    user_id: UUID


class WorkspaceUser(UserRead):
    user_role: list[GroupRole]


class UserWithTasks(WorkspaceUser):
    appointed_tasks: list[TaskRead] | None = None
