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
#   user_id: UUID
#   user_role: GroupRole = GroupRole.user.value    ?????  Как правильно создать enum
    # в схеме membership должны быть поля юзер_айди и юзер_рол как в модели


# классы юзер рид и юзер виз таскс может быть потом нужно будет перенести в другие модули
# нужно будет смотреть по логике
class UserRead(BaseModel):
    # id
    # full_name
    # role_in_ws: GroupRole
    pass


class UserWithTasks(UserRead):
    # tasks : list[Task]
    pass
