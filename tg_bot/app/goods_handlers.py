"""
Модуль для работы с продуктами

    Functions:
        add_good
        process_name_step
        process_brand_step
        process_nutritional_values_step
"""
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.keyboards import kb_no_brand
from app.models import AddGoodStates
from app.request_utils import add_good_request
from app.utils import str_good


async def add_good(message: Message, bot: AsyncTeleBot) -> None:
    """
    Функция запускается при отправки комадны в бот /new_good
    Начало процесса добавления данных продукта
    """
    await bot.send_message(
        message.chat.id,
        "Отправь название продукта",
    )
    await bot.set_state(message.from_user.id, AddGoodStates.name, message.chat.id)


async def process_name_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    1 шаг добавления продукта
    Функция принимает название продукта
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    await bot.send_message(
        message.chat.id, "Отправь бренд продукта", reply_markup=kb_no_brand()
    )
    await bot.delete_message(message.chat.id, message.message_id)

    await bot.set_state(message.from_user.id, AddGoodStates.brand, message.chat.id)


async def process_brand_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    2 шаг добавления продукта
    Функция добавляет бренд продукта
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text != "Без бренда":
            data["brand"] = message.text
    await bot.send_message(message.chat.id, "Напиши КБЖУ целыми числами через пробел")
    await bot.set_state(message.from_user.id, AddGoodStates.nutritional_values, message.chat.id)


async def process_nutritional_values_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    3 шаг добавления продукта
    Функция добавления пищевой ценности продукта
    Отправка запроса на сервис
    """
    if vals := str_to_int(message.text, 4):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["kcal"], data["proteins"], data["fats"], data["carbohydrates"] = vals
            good = str_good(await add_good_request(data))
        await bot.send_message(message.chat.id, good)
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(message.chat.id, "Напиши КБЖУ целыми числами через пробел")
        await bot.set_state(message.from_user.id, AddGoodStates.nutritional_values, message.chat.id)
