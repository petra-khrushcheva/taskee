from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(url=settings.DATABASE_URL, echo=settings.db_echo)

async_session = async_sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine,
                                   expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
