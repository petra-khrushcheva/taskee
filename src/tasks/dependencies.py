from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.tasks.models import Task
from src.tasks.services import TaskCRUD
from src.users.dependencies import current_active_user as current_user
from src.users.models import User
from src.workspaces.models import GroupRole
from src.workspaces.services import WSMembershipCRUD


async def get_ws_task_by_id(
        task_id: Annotated[UUID, Path],
        ws_id: Annotated[UUID, Path],
        session: AsyncSession = Depends(get_session)
):
    task = await TaskCRUD.get_ws_task(
        session=session, task_id=task_id, ws_id=ws_id
    )
    if task is not None:
        return task
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no task {task_id} in workspace {ws_id}"
        )


async def is_ws_admin_or_task_creator(
        ws_id: Annotated[UUID, Path],
        task: Task = Depends(get_ws_task_by_id),
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_session)
):
    if task.creator_id == user.id:
        return task
    user_role = await WSMembershipCRUD.get_user_role_in_ws(
        session=session, ws_id=ws_id, user=user
    )
    if user_role == GroupRole.admin.value:
        return task
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised to perform this action"
        )
