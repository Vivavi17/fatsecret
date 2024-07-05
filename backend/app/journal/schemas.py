import datetime

from pydantic import BaseModel, Field


class SAddNote(BaseModel):
    good_id: int
    weight: int
    date: str | datetime.date