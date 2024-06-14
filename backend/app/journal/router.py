from datetime import date

from fastapi import APIRouter, Depends

from app.journal.service import add_journal_note, find_average_kcal
from app.users.depends import user_rights

router = APIRouter(prefix="/journal", tags=["Journal"])


@router.post("/{user_id}")
async def add_note(
    good_id: int, weight: int, date: date = date.today(), user=Depends(user_rights)
):
    return await add_journal_note(user.id, date, good_id, weight)


@router.get("/{user_id}")
async def find_average_kcal_period(
    date_from: date = date.today(),
    date_to: date = date.today(),
    user=Depends(user_rights),
) -> int:
    return await find_average_kcal(date_from, date_to, user.id)
