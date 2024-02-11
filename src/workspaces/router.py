from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from workspaces.schemas import (
    WorkspaceRead, WorkspaceCreate, WorkspaceWithTasks, MembershipCreate
)
from workspaces.services import WorkspaceCRUD, WSMembershipCRUD
from workspaces.dependencies import (
    is_ws_member, get_workspace_by_id, is_ws_admin
)
from users.dependencies import get_user_by_id, current_active_user as get_user
from users.schemas import (
    UserRead, UserWithTasks
)   # какая юзер схема здесь на самом деле нужна???


"""Router for workspace CRUD"""
ws_router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

"""Router for working with associations of users and workspaces"""
membership_router = APIRouter(
    prefix="/workspaces/{ws_id}/members", tags=["Workspace Membership"]
)


@ws_router.post(
        "/", status_code=status.HTTP_201_CREATED, response_model=WorkspaceRead
    )
async def create_workspace(
    ws_data: WorkspaceCreate,
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(get_user),
):
    """Route for creating a workspace. Avaliable for any authenticated user"""
    return await WorkspaceCRUD.create_workspace(
        session=session, ws_data=ws_data, current_user=current_user
    )


@ws_router.get("/{id}", response_model=WorkspaceWithTasks)
async def get_workspace(
    id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(is_ws_member),
):
    """
    Route for retrieving a workspace with all its tasks.
    Avaliable for any member of that workspace
    """
    workspace = WorkspaceCRUD.get_workspace_with_tasks(
        id=id, current_user=current_user, session=session
    )
    return workspace


@ws_router.get("/", response_model=List[WorkspaceWithTasks])
async def get_workspaces(
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(get_user)
):
    """
    Route for retrieving all workspaces of a current user
    with 4 task of any workspace.
    Basically a front page route.
    Avaliable for any authenticated user.
    """
    return await WorkspaceCRUD.get_workspaces(
        session=session, current_user=current_user
    )


@ws_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace: WorkspaceRead = Depends(get_workspace_by_id),
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(is_ws_admin)
):
    """
    Route for deleting a workspace.
    Avaliable for any workspace admin.
    """
    return await WorkspaceCRUD.delete_workspace(
        session=session, workspace=workspace, current_user=current_user
    )


@ws_router.put(
        "/{id}", status_code=status.HTTP_200_OK, response_model=WorkspaceRead
    )
async def update_workspace(
    ws_data: WorkspaceCreate,
    workspace: WorkspaceRead = Depends(get_workspace_by_id),
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(is_ws_admin)
):
    """
    Route for updating workspace information,
    such as title and description.
    Avaliable for any workspace admin.
    """
    return await WorkspaceCRUD.update_workspace(
        session=session,
        workspace=workspace,
        ws_data=ws_data,
        current_user=current_user
    )


@membership_router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=List[UserRead],
    dependencies=[Depends(is_ws_admin)]
)
async def add_member_to_ws(
    workspace: WorkspaceRead = Depends(get_workspace_by_id),
    session: AsyncSession = Depends(get_session),
    added_user: MembershipCreate = Depends(get_user_by_id)
):
    """
    Route for adding user to workspace.
    Avaliable for any admin of that workspace.
    """
    return await WSMembershipCRUD.add_member_to_ws(
        session=session,
        workspace=workspace,
        added_user=added_user
    )
# здесь ошибка в логике. Где именно я передаю id добавляемого пользователя?


@membership_router.get(
        "/{user_id}",
        response_model=UserWithTasks,
        dependencies=[Depends(is_ws_member)]
    )
async def get_ws_member(
    workspace: WorkspaceRead = Depends(get_workspace_by_id),
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_user_by_id)
):
    """
    Route for retrieving any workspace member
    with all their tasks of that workspace.
    Avaliable for any member of that workspace.
    """
    return WSMembershipCRUD.get_ws_member(
        session=session,
        workspace=workspace,
        user=user
    )


@membership_router.get(
        "/",
        response_model=List[UserRead],
        dependencies=[Depends(is_ws_member)]
    )
async def get_all_ws_members(
    session: AsyncSession = Depends(get_session),
    workspace: WorkspaceRead = Depends(get_workspace_by_id)
):
    """
    Route for retrieving all workspace members
    with their workspace statuses.
    Avaliable for any member of that workspace.
    """
    return await WSMembershipCRUD.get_all_ws_members(
        session=session,
        workspace=workspace
    )


# удалить можно только юзера который уже член вс
@membership_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_from_ws(
    user: UserRead = Depends(get_user_by_id),
    workspace: WorkspaceRead = Depends(get_workspace_by_id),
    session: AsyncSession = Depends(get_session)
):
    """
    Route for deleting user from workspace.
    Avaliable for admin of that workspace or user themself.
    """
    return await WSMembershipCRUD.delete_member_from_ws(
        session=session,
        user=user,
        workspace=workspace
    )


# менять можно только статус юзера, который уже член воркспейса
@membership_router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[UserRead],
    dependencies=[Depends(is_ws_admin)]
)
async def update_ws_user_role(
    updated_ws_user: MembershipCreate = Depends(get_user_by_id),
    workspace: WorkspaceRead = Depends(get_workspace_by_id),
    session: AsyncSession = Depends(get_session),
):
    """
    Route for updating user status in the workspace.
    Avaliable for any admin of that workspace.
    """
    return await WSMembershipCRUD.update_ws_user_role(
        session=session,
        workspace=workspace,
        updated_ws_user=updated_ws_user
    )
