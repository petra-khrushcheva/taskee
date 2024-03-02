from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.users.dependencies import current_active_user as current_user
from src.users.models import User
from src.workspaces.models import GroupRole
from src.workspaces.services import WorkspaceCRUD, WSMembershipCRUD


async def is_user_in_workspace(
        user_id: UUID,
        ws_id: UUID,
        session: AsyncSession = Depends(get_session)
):
    """
    Checks if user is associated with workspace in any role.
    """
    user = await WSMembershipCRUD.get_ws_user(
        session=session, ws_id=ws_id, user_id=user_id
    )
    if user is not None:
        return user
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user {user_id} in workspace {ws_id}"
        )


async def is_ws_member(
        ws_id: Annotated[UUID, Path],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_session),
):
    """
    Checks if current user is associated with workspace in any role.
    """
    user = await is_user_in_workspace(
        session=session, ws_id=ws_id, user_id=user.id
    )
    return user


async def is_ws_admin(
        ws_id: Annotated[UUID, Path],
        user: User = Depends(is_ws_member),
        session: AsyncSession = Depends(get_session)
):
    """
    Checks if current user has admin rights.
    """
    user_role = await WSMembershipCRUD.get_user_role_in_ws(
        session=session, ws_id=ws_id, user=user
    )
    if user_role == GroupRole.admin.value:
        return user
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised to perform this action"
        )


async def is_ws_user(
        ws_id: Annotated[UUID, Path],
        user: User = Depends(is_ws_member),
        session: AsyncSession = Depends(get_session)
):
    """
    Checks if current user has workspace user rights.
    (Are they allowed to create tasks in this workspace).
    """
    user_role = await WSMembershipCRUD.get_user_role_in_ws(
        session=session, ws_id=ws_id, user=user
    )
    if user_role != GroupRole.reader.value:
        return user
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorised to perform this action"
        )


async def is_admin_or_self(
        user_id: Annotated[UUID, Path],
        ws_id: Annotated[UUID, Path],
        session: AsyncSession = Depends(get_session),
        user: User = Depends(is_ws_member)
):
    if user.id == user_id:
        return user
    return await is_ws_admin(ws_id=ws_id, user=user, session=session)


async def get_workspace_by_id(
        ws_id: Annotated[UUID, Path],
        session: AsyncSession = Depends(get_session)
):
    workspace = await WorkspaceCRUD.get_workspace(session=session, ws_id=ws_id)
    if workspace is not None:
        return workspace
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This workspace does not exist"
        )


async def get_ws_user_by_id(
        user_id: Annotated[UUID, Path],
        ws_id: Annotated[UUID, Path],
        session: AsyncSession = Depends(get_session)
):
    """
    Checks if user declared in the path
    is associated with workspace in any role.
    """
    return await is_user_in_workspace(
        session=session, ws_id=ws_id, user_id=user_id
    )
