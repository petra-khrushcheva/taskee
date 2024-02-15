from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager

from users.models import User
from workspaces.models import GroupRole, Workspace, WorkspaceUserAssociation
from workspaces.schemas import WorkspaceCreate, MembershipCreate
from tasks.models import Task


TASKS_PER_WS_FRONT_PAGE_LIMIT = 4


class WorkspaceCRUD():

    @staticmethod
    async def create_workspace(
        session: AsyncSession, ws_data: WorkspaceCreate, current_user: User
    ):
        workspace = Workspace(**ws_data.model_dump())
        workspace_role = WorkspaceUserAssociation(
            user=current_user, ws_role=GroupRole.admin.value
        )
        workspace.users.append(workspace_role)
        session.add(workspace)
        await session.commit()
        await session.refresh(workspace)
        return workspace

    @staticmethod
    async def get_workspace(session: AsyncSession, ws_id: UUID):
        return await session.get(Workspace, ws_id)

    @staticmethod
    async def get_workspace_with_tasks(
        session: AsyncSession,
        ws_id: UUID,
        # current_user: User
    ):
        stmt = (
            select(Workspace)
            .options(selectinload(Workspace.tasks))
            .filter_by(id=ws_id)
        )
        return await session.execute(stmt)
# после можно добавить функционал, показывающий,
# является ли каррент юзер исполнителем или создателем задачи.
# нужно ли здесь скалярс или олл???

    @staticmethod
    async def get_workspaces(session: AsyncSession, current_user: User):
        subq = (
            select(Task.id.label("task_id"))
            .filter(Task.workspace_id == Workspace.id)
            .order_by(Task.created_at.desc())
            .limit(TASKS_PER_WS_FRONT_PAGE_LIMIT)
            .scalar_subquery()  # я хз будет ли работать эта хуйня, может здесь просто сабкваери???
            .correlate(Workspace)
            )
        stmt = (
            select(Workspace)
            .join(WorkspaceUserAssociation)
            .join(Task, Task.id.in_(subq))
            .where(WorkspaceUserAssociation.user_id == current_user.id)
            .options(contains_eager(Workspace.tasks))
        )
        result: Result = await session.execute(stmt)
        workspaces = result.unique().scalars().all()
        return workspaces
# получить все воркспейсы с фильтрацией по айди керрент юзера,
# к каждому воркспейсу добавить четыре задачи из него
# Схема - Все группы + по 4 задачи в каждой группе
# после можно добавить функционал, показывающий,
# кто является исполнителем задачи.

    @staticmethod
    async def delete_workspace(
        session: AsyncSession, workspace: Workspace
    ):
        await session.delete(workspace)
        # workspace.is_active = False
        await session.commit()

    @staticmethod
    async def update_workspace(
        session: AsyncSession,
        workspace: Workspace,
        workspace_data: WorkspaceCreate
    ):
        for key, value in workspace_data.model_dump().items():
            setattr(workspace, key, value)
        await session.commit()
        return workspace
# Схема - ws_read (без списка задач)


class WSMembershipCRUD():

    @staticmethod
    async def add_member_to_ws(
        session: AsyncSession,
        workspace: Workspace,
        membership: MembershipCreate
    ):
        ws_membership = WorkspaceUserAssociation(**membership.model_dump())
        workspace.users.append(ws_membership)
        await session.commit()

# add member to ws
# добавленный пользователь получает статус юзера, если не указано другое
# схема - список членов группы со статусами, по идее в ручке можно
# использовать эту функцию и get_all_ws_members вместе

    @staticmethod
    async def get_ws_user(session: AsyncSession, ws_id: UUID, user_id: UUID):
        stmt = (
            select(User)
            .join(WorkspaceUserAssociation)
            .where(
                User.id == user_id,
                WorkspaceUserAssociation.workspace_id == ws_id
            )
        )
        user: Result = await session.execute(stmt)
        return user.scalar_one_or_none()

    @staticmethod
    async def get_user_role_in_ws(
        session: AsyncSession, user: User, ws_id: UUID
    ):
        stmt = (
            select(WorkspaceUserAssociation.user_role)
            .filter_by(user_id=user.id, workspace_id=ws_id)
        )
        user_role: Result = await session.execute(stmt)
        return user_role.scalar_one()  # ??? может и не скаляр, посмотрим на результат 


# get member получить одного
# доступность - любой член группы
# Схема - один член группы, со всеми его задачами _этой_ группы

    @staticmethod
    async def get_all_ws_members(session: AsyncSession, ws_id: UUID):
        stmt = select(Workspace)
        result: Result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks

# get members
# доступность - любой член группы
# Схема - Список Юзеров со статусами

    @staticmethod
    async def delete_member_from_ws(
        session: AsyncSession, workspace: Workspace, user: User
    ):
        await session.delete(task)
        await session.commit()
# добавить запрет на удаление единственного админа

    @staticmethod
    async def update_ws_user_role(
        session: AsyncSession,
        workspace: Workspace,
        membership: MembershipCreate,
        current_user: User
    ):
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        await session.commit()
        return task

# update member role
# Схема - список юзеров со статусами
