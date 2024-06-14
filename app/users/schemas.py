from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UsersRegister(UserAuth, BaseModel):
    sex: int
    age: int
    weight: int
    height: int
    desired_result: Literal["weight loss", "support", "mass gain"]
    activity_lvl: float
    daily_kcal: int
    id_tg: Optional[int] = None
    newsletter: Optional[int] = 0


class SUsers(UsersRegister, BaseModel):
    id: int


class SUsersUpgrade(UsersRegister, BaseModel):
    sex: Optional[int] = None
    age: Optional[int] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    desired_result: Literal["weight loss", "support", "mass gain"] = None
    activity_lvl: Optional[float] = None
    daily_kcal: Optional[int] = None
    id_tg: Optional[int] = None
    newsletter: Optional[int] = None
