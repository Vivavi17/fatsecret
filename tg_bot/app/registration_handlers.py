"""
Модуль с шагами регистрации пользователя

    Functions:
        start_handler
        registration_pressed
        process_email_step
        process_password_step
        process_sex_step
        process_age_weight_height_step
        process_activity_lvl_step
        process_desired_result_step
        process_notify_step
        process_end_register_step
"""
from config import activity, activity_lvls, desired_result
from keyboards import (kb_activity_lvls, kb_daily_kcal, kb_desired_result,
                       kb_fem_or_male, kb_y_or_n)
from app.models import UserStates, SUserRegister
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from app.utils import (calorie_calculation, str_to_int, valid_int)
from app.request_utils import registration_request, ping_user_request
from app.msgs import msg_user_exist, msg_send_mail, msg_err_send_mail


async def registration(message: Message, bot: AsyncTeleBot) -> None:
    """
    Функция запускается при отправки комадны в бот /registration, /"start
    Начало процесса регистрации нового пользователя, если пользователь не найден в базе
    """
    user = await ping_user_request(message.chat.id)
    if user:
        await bot.send_message(message.chat.id, msg_user_exist)
        return
    await bot.set_state(message.from_user.id, UserStates.email, message.chat.id)
    await bot.send_message(message.chat.id, msg_send_mail)


async def process_email_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    1 шаг регистрации
    Проверяет почту, просит ввести пароль
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            data["user"] = SUserRegister(email=message.text)
        except ValueError or AssertionError as e:
            err_msg = e.errors()[0]["msg"]
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, msg_err_send_mail(err_msg))
            await bot.set_state(message.from_user.id, UserStates.email, message.chat.id)
        else:
            await bot.send_message(message.chat.id, "Придумай пароль")
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.set_state(message.from_user.id, UserStates.password, message.chat.id)


async def process_password_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    2 шаг регистрации
    Добавляет пароль, удаляя сообщение от пользователя
    """
    await bot.send_message(message.chat.id, "Укажи пол", reply_markup=kb_fem_or_male())
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.set_state(message.from_user.id, UserStates.sex, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["password"] = message.text


async def process_sex_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    3 шаг регистрации
    Добавляет данные о поле юзера
    """
    if message.text in ("Мужской", "Женский"):
        await bot.send_message(
            message.chat.id, "Введи через пробел возраст(в годах), вес(в кг), рост(в см)"
        )
        await bot.set_state(
            message.from_user.id, UserStates.age_weight_height, message.chat.id
        )
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["sex"] = int(message.text == "Женский")
    else:
        await bot.send_message(message.chat.id, "Укажи пол", reply_markup=kb_fem_or_male())
        await bot.set_state(message.from_user.id, UserStates.sex, message.chat.id)


async def process_age_weight_height_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    4 шаг регистрации
    Добавляет корректные дынные о возрасте, весе и росте пользователя
    """
    if vals := str_to_int(message.text, 3):
        await bot.send_message(
            message.chat.id, "Выбери уровень активности:", reply_markup=kb_activity_lvls()
        )
        await bot.set_state(message.from_user.id, UserStates.activity_lvl, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["age"], data["weight"], data["height"] = vals
    else:
        await bot.send_message(
            message.chat.id, "Введи через пробел возраст(в годах), вес(в кг), рост(в см)"
        )
        await bot.set_state(
            message.from_user.id, UserStates.age_weight_height, message.chat.id
        )


async def process_activity_lvl_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    5 шаг регистрации
    Добавляет уровень активности пользователя
    """
    if message.text in activity_lvls:
        await bot.send_message(
            message.chat.id, "Выбери цель:", reply_markup=kb_desired_result()
        )
        await bot.set_state(
            message.from_user.id, UserStates.desired_result, message.chat.id
        )
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["activity_lvl"] = activity[message.text]
    else:
        await bot.send_message(
            message.chat.id, "Выбери уровень активности:", reply_markup=kb_activity_lvls()
        )
        await bot.set_state(message.from_user.id, UserStates.activity_lvl, message.chat.id)


async def process_desired_result_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    6 шаг регистрации
    Добавляет цель пользователя
    """
    if message.text in desired_result:
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["desired_result"] = desired_result[message.text]
            kcal = calorie_calculation(data)
        await bot.send_message(
            message.chat.id,
            f"Рекомендуемое потребление калорий: {kcal}ккал, но можете записать свое значение",
            reply_markup=kb_daily_kcal(kcal),
        )
        await bot.set_state(message.from_user.id, UserStates.daily_kcal, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id, "Выбери цель:", reply_markup=kb_desired_result()
        )
        await bot.set_state(
            message.from_user.id, UserStates.desired_result, message.chat.id
        )


async def process_daily_kcal_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    7 шаг регистрации
    Добавляет ежедневную цель калорий
    """
    if integer := valid_int(message.text):
        await bot.send_message(
            message.chat.id, "Хотите получать уведомления?", reply_markup=kb_y_or_n()
        )
        await bot.set_state(message.from_user.id, UserStates.newsletter, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["daily_kcal"] = integer
    else:
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            kcal = calorie_calculation(data)
        await bot.send_message(
            message.chat.id,
            f"Рекомендуемое потребление калорий: {kcal}ккал, но можете записать свое значение",
            reply_markup=kb_daily_kcal(kcal),
        )
        await bot.set_state(message.from_user.id, UserStates.daily_kcal, message.chat.id)


async def process_newsletter_step(message: Message, bot: AsyncTeleBot) -> None:
    """
    8 шаг регистрации
    Добавляет данные об уведомлениях
    """
    if message.text in ("Да", "Нет"):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["newsletter"] = int(message.text == "Да")
            data["id_tg"] = message.chat.id
            if response := await registration_request(data):
                await bot.send_message(message.chat.id, response)
        await bot.send_message(message.chat.id, f"Вы зарегестрировались")
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id, "Хотите получать уведомления?", reply_markup=kb_y_or_n()
        )
        await bot.set_state(message.from_user.id, UserStates.newsletter, message.chat.id)
