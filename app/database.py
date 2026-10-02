# app/database.py
from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Mapped
from fastapi import Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings, DatabaseTypeEnum
from contextlib import asynccontextmanager
from app.schemas.pagination import QueryParams
from app.models.base import Base
from app.utils import model_to_dict, apply_query_params
from app.utils import (
    CursedResponser,
    CursedException,
    check_resource_access,
    ResourceOperation,
    codes
)
import logging
import sys

logger = logging.getLogger(__name__)


if DatabaseTypeEnum.MYSQL == settings.db_type:
    DATABASE_URL = f"mysql+aiomysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
else:
    DATABASE_URL = None
    logger.critical("This database type not supported")
    sys.exit()

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.log_level.value == "DEBUG",
    pool_pre_ping=True,
    pool_recycle=3600
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def manual_get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_db() -> AsyncSession:
    logger.debug("get_db: opening new session")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
            logger.debug("get_db: session committed")
        except Exception as error:
            logger.debug(f"get_db: rolling back session due to {error}")
            await session.rollback()
            raise
        finally:
            logger.debug("get_db: closing session")
            await session.close()

async def db_delete_object(db: AsyncSession, obj: type[Base], by: Mapped[Any], id: int, not_raise: bool = False) -> Response:
    result_object = (await db.execute(select(obj).where(by == id))).scalar_one_or_none()

    if not result_object and not_raise is False:
        raise CursedException(code=codes.NOT_FOUND, error=f"Resource {id} not found", data={})

    elif result_object:
        await db.delete(result_object)

    # Важная логика. Если not_raise True то он не будет вызывать ошибку не найдено. 
    return CursedResponser(
        code=codes.DELETED,
        data={}
    )