from uuid import UUID
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from workspaces.models import Workspace, WorkspaceUserAssociation, GroupRole
from workspaces.schemas import WorkspaceCreate

from users.models import User


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
    async def get_workspace(
        session: AsyncSession, id: UUID, current_user: User
    ):
        return await session.get(Workspace, id)
    # здесь нужно разрешение для членов группы, но разрешение 
    # определяется зависимостью в пути, а здесь только работа с базой данных

    # зависимость берет айди текущего юзера, айди воркспейса и проверяет,
    # есть ли мэтч в ассоциативной таблице, если нет - возвращает ошибку,
    # такую зависимость можно добавить в зависимости декоратора, а не пути

    @staticmethod
    async def get_workspace_with_tasks(
        session: AsyncSession, id: UUID, current_user: User
    ):
        stmt = (
            select(Workspace)
            .options(selectinload(Workspace.tasks))
            .filter_by(id=id, is_active=True)
        )
        return await session.execute(stmt)

# нужно ли здесь скалярс или олл???
# здесь нужно разрешение для членов группы

    @staticmethod
    async def get_workspaces(session: AsyncSession, current_user: User):
# получить все воркспейсы с фильтрацией по айди керрент юзера,
# к каждому воркспейсу добавить четыре задачи из него
        stmt = select(Workspace)
        result: Result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks
# get workspaces
# доступность - фильтрация в ассоциативной таблице по айди юзера, отдельных разрешений не нужно
# Схема - Все группы + по 4 задачи в каждой группе


    @staticmethod
    async def delete_workspace(
        session: AsyncSession, workspace: Workspace, current_user: User
    ):
        await session.delete(task)
        await session.commit()
# здесь нужно закомментить строку с удалением воркспейса и создать изменение параметра из_актив
# также здесь нужно разрешение только для админов 
# delete workspace
# доступность - is_ws_admin
# Схема - без схемы, просто статус код



    @staticmethod
    async def update_workspace(session: AsyncSession,
                          workspace: Task,
                          workspace_data: TaskCreate,
                          current_user: User):
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        await session.commit()
        return task
# здесь нужно разрешение только для админов 
# update workspace
# доступность - is_ws_admin
# Схема - ws_read (без списка задач)


class WSMembershipCRUD():

    @staticmethod
    async def add_member_to_ws(
        session: AsyncSession, ws_data: WorkspaceCreate, added_user: User
    ):

        #     workspace = Workspace(**ws_data.model_dump())
        #     workspace_role = WorkspaceUserAssociation(
        #         user=current_user, ws_role=GroupRole.admin.value
        #     )
        #     workspace.users.append(workspace_role)
        #     session.add(workspace)
        #     await session.commit()
        #     await session.refresh(workspace)
        #     return workspace
        pass
# add member to ws
# доступность - админ группы
# добавленный пользователь получает статус юзера, если не указано другое
# схема - список членов группы со статусами

    @staticmethod
    async def get_ws_member(
        session: AsyncSession, id: UUID, current_user: User
    ):
        return await session.get(Workspace, id)
    # здесь нужно разрешение для членов группы, но разрешение 
    # определяется зависимостью в пути, а здесь только работа с базой данных

    # зависимость берет айди текущего юзера, айди воркспейса и проверяет,
    # есть ли мэтч в ассоциативной таблице, если нет - возвращает ошибку,
    # такую зависимость можно добавить в зависимости декоратора, а не пути
# get member получить одного
# доступность - любой член группы
# Схема - один член группы, со всеми его задачами _этой_ группы

    @staticmethod
    async def get_all_ws_members(session: AsyncSession, current_user: User):
# получить все воркспейсы с фильтрацией по айди керрент юзера,
# к каждому воркспейсу добавить четыре задачи из него
        stmt = select(Workspace)
        result: Result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks
# get workspaces
# доступность - фильтрация в ассоциативной таблице по айди юзера, отдельных разрешений не нужно
# Схема - Все группы + по 4 задачи в каждой группе
    
    # get members
# доступность - любой член группы
# Схема - Список Юзеров со статусами


    @staticmethod
    async def delete_member_from_ws(
        session: AsyncSession, workspace: Workspace, user: User
    ):
        await session.delete(task)
        await session.commit()
# здесь нужно закомментить строку с удалением воркспейса и создать изменение параметра из_актив
# также здесь нужно разрешение только для админов 
# delete workspace
# доступность - is_ws_admin
# Схема - без схемы, просто статус код
# добавить запрет на удаление единственного админа



    @staticmethod
    async def update_workspace(session: AsyncSession,
                          workspace: Task,
                          workspace_data: TaskCreate,
                          current_user: User):
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        await session.commit()
        return task
# здесь нужно разрешение только для админов 
# update workspace
# доступность - is_ws_admin
# Схема - ws_read (без списка задач)


