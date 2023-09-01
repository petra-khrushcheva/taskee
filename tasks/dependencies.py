from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from tasks.crud import TaskCRUD


async def get_tasks_crud(
        session: AsyncSession = Depends(get_session)
) -> TaskCRUD:
    return TaskCRUD(session=session)
