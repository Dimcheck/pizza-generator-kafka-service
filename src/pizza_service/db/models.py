from typing import List

from db.session import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(50))

    # orders: Mapped[List["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "order"

    uuid: Mapped[str] = mapped_column(String(50), unique=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    pizzas: Mapped[dict] = mapped_column(MutableList.as_mutable(JSON), default=list)
    movie_ticket: Mapped[dict] = mapped_column(JSON, nullable=True, default=dict)

    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # user: Mapped["User"] = relationship(back_populates="orders")

    @classmethod
    async def update(cls, db: AsyncSession, column_name: str, column_value: str, **kwargs):
        try:
            target_obj = await cls.get_by_column(db, column_name, column_value)
        except NoResultFound:
            return

        for key, value in kwargs.items():
            setattr(target_obj, key, value)

        db.add(target_obj)
        await db.commit()
        await db.refresh(target_obj)
        return target_obj



