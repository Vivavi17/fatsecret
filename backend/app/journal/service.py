from datetime import date

from app.exceptions import NotFoundByDateException, NotFoundException
from app.goods.dao import GoodsDao
from app.journal.dao import JournalDao


async def add_journal_note(user_id: int, date: date, good_id: int, weight: int):
    if not (good := GoodsDao.find_one_or_none(id=good_id)):
        raise NotFoundException
    return await JournalDao.add_row(
        user_id=user_id, date=date, good_id=good_id, weight=weight
    )


async def find_average_kcal(date_from: date, date_to: date, user_id: int) -> int:
    avg_kcal = await JournalDao.find_kcal(date_from, date_to, user_id)
    if not avg_kcal:
        raise NotFoundByDateException
    return int(avg_kcal)
