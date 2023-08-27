import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
