"""
Модуль для работы с записями личного дневника

    Functions:
        add_note
        process_name_goods_step
        process_id_goods_step
        process_goods_weight_step
        process_goods_date_step

        find_average_kcal_period
        process_date_from_step
        process_date_to_step
"""
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.keyboards import kb_date, kb_list_goods
from app.models import AverageKcalStates, GoodStates
from app.request_utils import add_note_request, find_average_kcal_request, find_good_request
from app.utils import valid_date


async def add_note(message: Message, bot: AsyncTeleBot) -> None:
    """
    Функция запускается при отправки комадны в бот /add_note
    Начало процесса добавления записи о приеме пищи в журнал
    """
    await bot.send_message(
        message.chat.id,
        "Отправь название продукта",
    )
    await bot.set_state(message.from_user.id, GoodStates.name, message.chat.id)


async def process_name_goods_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    1 шаг добавления записи в журнал
    Функция принимает название продукта, отправляет запрос на сервис
    Возвращает пользователю ответ в сообщении
    """
    goods = await find_good_request(message.text)
    if not goods:
        await bot.send_message(
            message.chat.id,
            "Ничего не найдено, создайте новый продукт /new_good",
        )
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id,
            "Вот список найденых продутов, выберите подходящий или создайте новый /new_good",
            reply_markup=kb_list_goods(goods),
        )
        await bot.set_state(message.from_user.id, GoodStates.id, message.chat.id)


async def process_id_goods_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    2 шаг добавления записи в журнал
    Функция добавляет Id продукта
    """
    if integer := valid_int(message.text.split(':')[0]):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["good_id"] = integer
        await bot.send_message(message.chat.id, "Напишите вес в граммах")
        await bot.set_state(message.from_user.id, GoodStates.weight, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id,
            "Отправь название продукта",
        )
        await bot.set_state(message.from_user.id, GoodStates.name, message.chat.id)


async def process_goods_weight_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    3 шаг добавления записи в журнал
    Функция добавляет вес продукта
    """
    if integer := valid_int(message.text):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["weight"] = integer
        await bot.send_message(
            message.chat.id, "Напишите дату в формате гггг-мм-дд", reply_markup=kb_date()
        )
        await bot.set_state(message.from_user.id, GoodStates.date, message.chat.id)
    else:
        await bot.send_message(message.chat.id, "Напишите вес в граммах")
        await bot.set_state(message.from_user.id, GoodStates.weight, message.chat.id)


async def process_goods_date_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    4 шаг добавления записи в журнал
    Функция добавляет дату приема пищи, отправляет полученые данные на сервис
    """
    if date := valid_date(message.text):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["date"] = date
            data["telegram_id"] = int(message.chat.id)
            await add_note_request(data)
        await bot.send_message(message.chat.id, "Запись добавлена", reply_markup=kb_date())
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id, "Напишите дату в формате гггг-мм-дд", reply_markup=kb_date()
        )
        await bot.set_state(message.from_user.id, GoodStates.date, message.chat.id)


async def find_average_kcal_period(message: Message, bot: AsyncTeleBot) -> None:
    """
    Функция запускается при отправки комадны в бот /average_kcal
    Начало процесса подсчета средних значений КБЖУ
    """
    await bot.send_message(
        message.chat.id,
        "Напиши дату начала периода в формате гггг-мм-дд", reply_markup=kb_date()
    )
    await bot.set_state(message.from_user.id, AverageKcalStates.date_from, message.chat.id)


async def process_date_from_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    1 шаг подсчета КБЖУ
    Функция добавляет дату начала периода
    """
    if date := valid_date(message.text):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["date_from"] = date
        await bot.send_message(
            message.chat.id,
            "Напиши дату окончания периода в формате гггг-мм-дд", reply_markup=kb_date()
        )
        await bot.set_state(message.from_user.id, AverageKcalStates.date_to, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id,
            "Напиши дату начала периода в формате гггг-мм-дд", reply_markup=kb_date()
        )
        await bot.set_state(message.from_user.id, AverageKcalStates.date_from, message.chat.id)


async def process_date_to_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    2 шаг подсчета КБЖУ
    Функция добавляет дату окончания периода, отправляет запрос на сервис
    Отправляет полученые данные пользователю
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        date_from = data["date_from"]
    if (date := valid_date(message.text)) and date_from <= date:
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["date_to"] = date
            data["telegram_id"] = int(message.chat.id)
            kcal, proteins, fats, carbohydrates = (await find_average_kcal_request(data)).values()
            if data['date_from'] == data['date_to']:
                msg = f"КБЖУ за {data['date_from']}: {kcal}/{proteins}/{fats}/{carbohydrates}"
            else:
                msg = f"КБЖУ за {data['date_from']} - {data['date_to']}: {kcal}/{proteins}/{fats}/{carbohydrates}"
            await bot.send_message(message.chat.id, msg)
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id,
            "Напиши дату окончания периода в формате гггг-мм-дд", reply_markup=kb_date()
        )
        await bot.set_state(message.from_user.id, AverageKcalStates.date_to, message.chat.id)
