"""
В модуле описываются классы для процессов бота

    Classes:
        UserStates
        GoodStates
        AverageKcalStates
        AddGoodStates
"""
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field
from telebot.asyncio_handler_backends import State, StatesGroup

class SUserRegister(BaseModel):
    email: EmailStr = "user@example.com"
    password: str = Field(default="password", min_length=6)
    sex: Literal[0, 1] = 0
    age: int = Field(default=1, gt=0)
    weight: int = Field(default=1, gt=0)
    height: int = Field(default=1, gt=0)
    desired_result: Literal["weight loss", "support", "mass gain"] = "support"
    activity_lvl: float = Field(default=1.2, gt=0.0)
    daily_kcal: int = Field(default=1, gt=0)
    id_tg: Optional[int] = None
    newsletter: Literal[0, 1] = 0

class UserStates(StatesGroup):
    """Запоминает шаги пользователя при регистрации"""
    email = State()
    password = State()
    sex = State()
    age_weight_height = State()
    desired_result = State()
    activity_lvl = State()
    daily_kcal = State()
    newsletter = State()


class GoodStates(StatesGroup):
    """Запоминает статус пользователя при добавлении новой записи в журнал"""
    name = State()
    id = State()
    weight = State()
    date = State()
    id_tg = State()


class AverageKcalStates(StatesGroup):
    """Запоминает шаги пользователя при подсчете КБЖУ"""
    date_from = State()
    date_to = State()


class AddGoodStates(StatesGroup):
    """Запоминает шаги пользователя при добавлении новых продутов"""
    name = State()
    brand = State()
    nutritional_values = State()
