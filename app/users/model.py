from typing import Literal, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.datebase import Base


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    sex: Mapped[int]
    age: Mapped[int]
    weight: Mapped[int]
    height: Mapped[int]
    desired_result: Mapped[Literal["weight loss", "support", "mass gain"]]
    activity_lvl: Mapped[float]
    daily_kcal: Mapped[int]
    id_tg: Mapped[Optional[int]]
    newsletter: Mapped[Optional[int]]

    journal: Mapped[list["Journal"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return f"User {self.email}"
