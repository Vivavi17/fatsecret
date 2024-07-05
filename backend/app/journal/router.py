from datetime import date, datetime

from fastapi import APIRouter, Depends

from app.journal.schemas import SAddNote
from app.journal.service import add_journal_note, find_average_kcal
from app.journal.utils import check_data
from app.users.depends import user_rights

router = APIRouter(prefix="/journal", tags=["Journal"])


@router.post("")
async def add_note(
        data: SAddNote, user=Depends(user_rights)
):
    data.date = check_data(data.date)
    return await add_journal_note(user.id, data.date, data.good_id, data.weight)


@router.get("/average_kcal_period")
async def find_average_kcal_period(
        date_from: str | date = date.today(),
        date_to: str | date = date.today(),
        user=Depends(user_rights),
):
    date_from = check_data(date_from)
    date_to = check_data(date_to)
    return await find_average_kcal(date_from, date_to, user.id)
