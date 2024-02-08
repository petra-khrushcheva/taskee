from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from workspaces.schemas import (
    WorkspaceRead, WorkspaceCreate, WorkspaceWithTasks
)
from workspaces.services import WorkspaceCRUD, WSMembershipCRUD
from workspaces.dependencies import (
    is_ws_member, get_workspace_by_id, is_ws_admin)
from users.dependencies import current_active_user as get_user
from users.schemas import (
    UserRead,
)  # будут ли работать ручки, если они получают схему, а не модель?
# и эта ли схема здесь нужна???


"""Router for workspace CRUD"""
ws_router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

"""Router for working with associations of users and workspaces"""
membership_router = APIRouter(
    prefix="/workspaces/{ws_id}/members", tags=["Workspace Membership"]
)     # или просто id????


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
    added_user: UserRead = Depends(get_user_by_id) # написать эту зависимость
):
    return await WSMembershipCRUD.add_member_to_ws(
        session=session,
        task_data=task_data)


# add member to ws
# доступность - админ группы
# добавленный пользователь получает статус юзера, если не указано другое
# схема - список членов группы со статусами


@membership_router.get("/{id}", response_model=schemas.Task)
async def get_task(task: Task = Depends(get_task_by_id)):
    return task


# get member получить одного
# доступность - любой член группы
# Схема - один член группы, со всеми его задачами _этой_ группы


@membership_router.get("/", response_model=List[schemas.Task])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    return await WSMembershipCRUD.get_tasks(session=session)


# get members
# доступность - любой член группы
# Схема - Список Юзеров со статусами


@membership_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Task = Depends(get_task_by_id), session: AsyncSession = Depends(get_session)
):
    return await WSMembershipCRUD.delete_task(session=session, task=task)


# delete member
# доступность - is_ws_admin or self
# Схема - без схемы, просто статус код
# возможно редирект на страницу со всеми воркспейсами


@membership_router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Task
)
async def update_task(
    task_data: schemas.TaskCreate,
    task: Task = Depends(get_task_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await WSMembershipCRUD.update_task(session=session, task=task, task_data=task_data)


# update member role
# доступность - is_ws_admin
# Схема - список юзеров со статусами
