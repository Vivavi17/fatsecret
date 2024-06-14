from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.datebase import Base


class Goods(Base):
    __tablename__ = "goods"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    brand: Mapped[Optional[str]]
    proteins: Mapped[int]
    fats: Mapped[int]
    carbohydrates: Mapped[int]
    kcal: Mapped[int]

    journal: Mapped["Journal"] = relationship(back_populates="good")

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.kcal}/{self.proteins}/{self.fats}/{self.carbohydrates}"
        )
