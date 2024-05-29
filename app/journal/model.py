from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date
from app.datebase import Base


class Journal(Base):
    __tablename__ = "journal"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date] = mapped_column(Date)
    good_id: Mapped[int] = mapped_column(ForeignKey("goods.id"))
    weight: Mapped[int]