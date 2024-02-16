from uuid import UUID
from sqlalchemy import desc, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from tasks.models import Task
from tasks.schemas import TaskCreate


class TaskCRUD():

    @staticmethod
    async def create_task(session: AsyncSession, task_data: TaskCreate):
        task = Task(**task_data.model_dump())
        # task.creator = ... или task = Post(creator_id=current_user.id, **task_data.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def get_ws_task(session: AsyncSession, ws_id: UUID, task_id: UUID):
        stmt = (
            select(Task)
            .options(
                joinedload(Task.creator),
                joinedload(Task.executor),
            ).where(
                Task.id == task_id,
                Task.workspace_id == ws_id
            )
        )
        user: Result = await session.execute(stmt)
        return user.scalar_one_or_none()

    @staticmethod
    async def get_tasks(session: AsyncSession):
        stmt = (select(Task)
                .options(
                joinedload(Task.creator),
                joinedload(Task.executor),
            ).where(
                Task.id == task_id,
                Task.workspace_id == ws_id
            ).order_by(desc(Task.created_at))
                )
        result: Result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks

    @staticmethod
    async def get_task(session: AsyncSession, id: int):
        return await session.get(Task, id)

    @staticmethod
    async def delete_task(session: AsyncSession, task: Task):
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def update_task(session: AsyncSession,
                          task: Task,
                          task_data: TaskCreate):
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        await session.commit()
        return task
