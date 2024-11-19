import contextlib
from typing import Annotated, Any, AsyncIterator, List, Optional

from configs.settings import settings
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    async def get_all(cls, db: AsyncSession):
        query = await db.execute(select(cls))
        return query.scalars().all()

    @classmethod
    async def get_by_column(cls, db: AsyncSession, column_name: str, column_value:str, many: bool = True):
        filter_condition = getattr(cls, column_name) == column_value
        query = select(cls).where(filter_condition)
        result = await db.execute(query)

        if many:
            return result.scalars().all()
        return result.scalar_one()

    @classmethod
    async def get_by_column_in(cls, db: AsyncSession, column_name: str, column_value: List[str]):
        filter_condition = getattr(cls, column_name).in_(column_value)
        query = select(cls).where(filter_condition)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get(cls, db: AsyncSession, id: int):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return
        return transaction

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        transaction = cls(**kwargs)

        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def update(cls, db: AsyncSession, id: int, **kwargs):
        try:
            target_obj = await db.get(cls, id)
        except NoResultFound:
            return

        for key, value in kwargs.items():
            setattr(target_obj, key, value)

        db.add(target_obj)
        await db.commit()
        await db.refresh(target_obj)
        return target_obj

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        try:
            target_obj = await db.get(cls, id)
            transaction = await db.delete(target_obj)
        except (NoResultFound, IntegrityError):
            return

        await db.commit()
        await db.refresh(transaction)
        return transaction


class DatabaseSessionManagerNotInitializedError(Exception):
    """DatabaseSessionManager is not initialized"""


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: Optional[dict[str, Any]] = None):
        if not engine_kwargs:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise DatabaseSessionManagerNotInitializedError()
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseSessionManagerNotInitializedError()

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseSessionManagerNotInitializedError()

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.DATABASE_URL,)


async def get_db():
    async with sessionmanager.session() as session:
        yield session


DB_DEPENDENCY = Annotated[AsyncSession, Depends(get_db)]



