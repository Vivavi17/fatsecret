from sqlalchemy import or_, select

from app.dao.base import BaseDAO
from app.datebase import async_session_maker
from app.goods.model import Goods


class GoodsDao(BaseDAO):
    model = Goods

    @classmethod
    async def find_by_name(cls, name: str) -> Goods | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter(or_(cls.model.name.ilike(f"%{name}%"), cls.model.brand.ilike(f"%{name}%")))
            result = await session.execute(query)
            return result.scalars().all()
