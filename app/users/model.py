from typing import Optional, Literal
from sqlalchemy.orm import Mapped, mapped_column

from app.datebase import Base


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    sex: Mapped[int]
    age: Mapped[int]
    weight: Mapped[int]
    height: Mapped[int]
    desired_result: Mapped[Literal["weight loss", "support", "mass gain"]]
    activity_lvl: Mapped[int]
    daily_kkal: Mapped[int]
    id_tg: Mapped[Optional[int]]
    newsletter: Mapped[Optional[int]]