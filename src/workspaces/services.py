from sqlalchemy import desc, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from workspaces.models import Workspace
from workspaces.schemas import WorkspaceCreate


class WorkspaceCRUD():

    @staticmethod
    async def create_workspace(session: AsyncSession, task_data: TaskCreate):
        task = Task(**task_data.model_dump())
        # task.creator = ... или task = Post(creator_id=current_user.id, **task_data.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def get_workspaces(session: AsyncSession):
        # stmt = (select(Task)
        #         .options(
        #             joinedload(Task.creator),
        #             joinedload(Task.executor),
        #         ).order_by(desc(Task.created_at)))
        stmt = select(Workspace)
        result: Result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks

    @staticmethod
    async def get_workspace(session: AsyncSession, id: int):
        return await session.get(Task, id)

    @staticmethod
    async def delete_workspace(session: AsyncSession, task: Task):
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def update_workspace(session: AsyncSession,
                          task: Task,
                          task_data: TaskCreate):
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        await session.commit()
        return task
