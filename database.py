import os
from dotenv import load_dotenv

from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session






























# import os
# from dotenv import load_dotenv
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# from sqlmodel import create_engine, SQLModel, Session

# load_dotenv()

# SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# SessionLocal = async_sessionmaker(bind=engine)


# def init_db():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# class Base(DeclarativeBase):
#     pass
