from sqlalchemy import insert, select

from app.datebase import Base, async_session_maker
from app.exceptions import NotFoundUpdateException


class BaseDAO:
    model = None

    @classmethod
    async def add_row(cls, **kwargs: dict) -> Base:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def find_one_or_none(cls, **filter_by: dict) -> Base | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by: dict) -> Base | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update_row(cls, id: int, data_update: dict) -> Base:
        async with async_session_maker() as session:
            object_db = await session.get(cls.model, id)
            if not object_db:
                raise NotFoundUpdateException

            for key, value in data_update.items():
                setattr(object_db, key, value)
            await session.commit()
            await session.flush()
            return object_db
