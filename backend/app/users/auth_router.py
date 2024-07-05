from fastapi import APIRouter, Depends, Response

from app.users.depends import get_curent_user, user_rights
from app.users.schemas import SUsers, UserAuth, UsersRegister
from app.users.service import (auth_user, create_cookies, del_cookie,
                               register_user)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(users_data: UsersRegister) -> SUsers:
    return await register_user(users_data)


@router.post("/login")
async def login(response: Response, data: UserAuth) -> str:
    user = await auth_user(data)
    access_token, refresh_token = await create_cookies(user.id, user.email)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return refresh_token


@router.post("/logout")
async def logout(response: Response, user=Depends(get_curent_user)) -> None:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    await del_cookie(user.email)


@router.post("/refresh")
async def refresh_token(response: Response, user=Depends(get_curent_user)) -> str:
    access_token, refresh_token = await create_cookies(user.id, user.email)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return refresh_token


@router.get("/ping_me")
def ping(user=Depends(user_rights)) -> str | None:
    if user:
        return f"User id:{user.id} ping!"
