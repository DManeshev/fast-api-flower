from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL
)

async_session_marker = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

class Base(AsyncAttrs, DeclarativeBase):
    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

async def get_async_session():
    async with async_session_marker() as session:
        yield session

PrimaryKey = Annotated[int, Field(gt=0, lt=2147483647)]

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]