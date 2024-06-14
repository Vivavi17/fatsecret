import jwt
from config import settings
from fastapi import Depends, Request
from users.dao import UsersDAO


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    return token


async def get_curent_user(token=Depends(get_refresh_token)):
    payload = jwt.decode(token, settings.secret, settings.algorithm)
    user_id = payload.get("sub")
    if not user_id:
        raise jwt.InvalidTokenError
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise jwt.InvalidTokenError
    return user


def get_access_token(request: Request):
    token = request.cookies.get("access_token")
    return token


async def user_rights(token=Depends(get_access_token)):
    payload = jwt.decode(token, settings.secret, settings.algorithm)
    user_id = payload.get("sub")
    if not user_id:
        raise jwt.InvalidTokenError
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise jwt.InvalidTokenError
    return user
