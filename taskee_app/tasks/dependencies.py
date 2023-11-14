from typing import Annotated
from uuid import UUID

from database import get_session
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.services import TaskCRUD


async def get_task_by_id(
        id: Annotated[UUID, Path],
        session: AsyncSession = Depends(get_session)
):
    task = await TaskCRUD.get_task(session=session, id=id)
    if task is not None:
        return task
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This task does not exist"
        )

    # if task.creator != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action"
    #     )
