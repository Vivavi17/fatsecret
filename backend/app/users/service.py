from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.cache import cache
from app.exceptions import IncorretLoginOrPasswordException, UserAlreadyExistException
from app.users.dao import UsersDAO
from app.users.schemas import SUsers, SUsersUpgrade, UserAuth, UsersRegister

hash = CryptContext(schemes=["bcrypt"], deprecated="auto").hash
verify = CryptContext(schemes=["bcrypt"], deprecated="auto").verify


def get_hash_password(password: str) -> str:
    return hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return verify(password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    if to_encode["type"] == "access":
        expire = datetime.now() + timedelta(minutes=1)
    else:
        expire = datetime.now() + timedelta(days=settings.token_life)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, settings.secret, settings.algorithm)
    return encoded_token.decode("utf-8")


async def create_cookies(user_id: int, user_email: str) -> tuple[str]:
    access_token = create_token({"type": "access", "sub": str(user_id)})
    refresh_token = create_token({"type": "refresh", "sub": str(user_id)})
    await cache.setex(user_email, timedelta(days=settings.token_life), refresh_token)
    return (access_token, refresh_token)


async def del_cookie(user_email: str) -> None:
    await cache.delete(user_email)


async def find_user_by_email(email: EmailStr):
    return await UsersDAO.find_one_or_none(email=email)


async def auth_user(data: UserAuth) -> SUsers:
    user = await find_user_by_email(data.email)
    if not (user and verify_password(data.password, user.password)):
        raise IncorretLoginOrPasswordException
    return user


async def register_user(users_data: UsersRegister) -> SUsers:
    is_exist = await find_user_by_email(users_data.email)
    if is_exist:
        raise UserAlreadyExistException
    users_data.password = get_hash_password(users_data.password)
    return await UsersDAO.add_row(**dict(users_data))


async def update_user(user_id: int, data: SUsersUpgrade) -> SUsers:
    data = data.model_dump(exclude_unset=True)
    return await UsersDAO.update_row(user_id, data)


async def save_tg_id_by_email(email: str, chat_id: int) -> SUsers:
    user = find_user_by_email(email)
    if user:
        return await UsersDAO.update_row(user.id, {"id_tg": chat_id})
