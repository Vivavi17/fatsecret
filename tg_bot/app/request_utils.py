"""
Модуль с запросами к бекенду

    Functions:
        registration_request
        find_good_request
        add_note_request
        find_average_kcal_request
        ping_user_request
        add_good_request
"""

import json

import requests

from app.config import db_url


async def registration_request(data: dict) -> str | None:
    """Запрос на регистрацию нового пользователя"""
    response = requests.post(
        db_url + "/auth/register", data=json.dumps(data)
    ).json()
    if detail := response.get('detail', None):
        return detail[0].get('msg', None)


async def find_good_request(name: str) -> list[dict]:
    """Поиск продуктов в БД"""
    response = requests.get(
        db_url + "/goods", params={"name": name}).json()
    return response


async def add_note_request(data: dict) -> dict:
    """Добавление записи о приеме пищи в БД"""
    tg_id = data.pop("telegram_id")
    response = requests.post(
        db_url + "/journal", params={"telegram_id": tg_id}, data=json.dumps(data)
    ).json()
    return response


async def find_average_kcal_request(data: dict) -> dict:
    """Получает КБЖУ за выбранный период"""
    response = requests.get(
        db_url + "/journal/average_kcal_period", params=data
    ).json()
    return response


async def ping_user_request(tg_id: str) -> str | None:
    """Проверяет, есть ли пользователь из чата в БД"""
    response = requests.get(
        db_url + "/auth/ping_me", params={"telegram_id": tg_id}).json()
    return response


async def add_good_request(data: dict) -> dict:
    """Добавляет в БД новый продукт,если не находит по указанным параметрам,
    затем возвращает его"""
    response = requests.post(
        db_url + "/goods", data=json.dumps(data)).json()
    return response
