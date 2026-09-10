from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(
    url=DATABASE_URL
)

async_session_marker = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_async_session():
    async with async_session_marker() as session:
        yield session

