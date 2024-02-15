from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
# from users.dependencies import current_active_user as get_user
from workspaces.services import WorkspaceCRUD


async def is_user_in_workspace(
        user_id: UUID,
        ws_id: UUID,
        session: AsyncSession = Depends(get_session)
    ):
    # здесь будет функция из круда, находящая в базе данных пользователя принадлежащего к группе
    # а здесь будет прописана ошибка, если он - None







# id во всех ручках надо прописать как ws_id, чтобы можно было везде
# использовать одну и ту же зависимость
# и здесь тоже
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


async def is_ws_member():
    pass
# если юзер не член этого воркспейса - You ara not authorised to work in this workspace

    # if task.creator != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action"
    #     )

    # зависимость берет айди текущего юзера, айди воркспейса и проверяет,
    # есть ли мэтч в ассоциативной таблице, если нет - возвращает ошибку,
    # такую зависимость можно добавить в зависимости декоратора, а не пути


async def is_ws_admin():
    pass


# возможно зависимость is_ws_member() нужно строить от просто юзера, а не от current user-a, потому что тогда ее можно будет использовать в updayr и delete membership
