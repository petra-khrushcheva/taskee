from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from users.models import User
from fastapi_users.db import SQLAlchemyUserDatabase


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
