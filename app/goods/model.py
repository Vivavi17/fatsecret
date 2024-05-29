from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.datebase import Base


class Goods(Base):
    __tablename__ = "goods"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    brand: Mapped[Optional[str]]
    proteins: Mapped[int]
    fats: Mapped[int]
    carbohydrates: Mapped[int]
    kkal: Mapped[int]
