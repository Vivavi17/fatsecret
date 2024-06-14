from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.datebase import Base


class Journal(Base):
    __tablename__ = "journal"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date] = mapped_column(Date)
    good_id: Mapped[int] = mapped_column(ForeignKey("goods.id"))
    weight: Mapped[int]

    user: Mapped["Users"] = relationship(back_populates="journal")
    good: Mapped["Goods"] = relationship(back_populates="journal")
