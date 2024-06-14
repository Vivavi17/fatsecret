from datetime import date

from sqlalchemy import func, select

from app.dao.base import BaseDAO
from app.datebase import async_session_maker
from app.goods.model import Goods
from app.journal.model import Journal


class JournalDao(BaseDAO):
    model = Journal

    @classmethod
    async def find_kcal(
        cls, date_from: date, date_to: date, user_id: int
    ) -> int | None:
        async with async_session_maker() as session:
            sum_kcal_from_period = (
                select(
                    cls.model.date,
                    (func.sum(cls.model.weight * Goods.kcal) / 100).label(
                        "kcal_on_day"
                    ),
                )
                .select_from(cls.model)
                .where(
                    cls.model.user_id == user_id,
                    cls.model.date >= date_from,
                    cls.model.date <= date_to,
                )
                .join(Goods, cls.model.good_id == Goods.id, isouter=True)
                .group_by(cls.model.date)
                .cte("sum_kcal_from_period")
            )

            avg_on_days = select(
                func.avg(sum_kcal_from_period.c.kcal_on_day)
            ).select_from(sum_kcal_from_period)

            result = await session.execute(avg_on_days)
            return result.scalar()
