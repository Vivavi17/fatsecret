from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot import types
from cache import cache
from config import activity_lvls, activity
from utils import calorie_calculation
from keyboards import (
    kb_fem_or_male,
    kb_activity_lvls,
    kb_desired_result,
    kb_daily_kcal,
    kb_y_or_n,
)
from models import UserStates


async def start_handler(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id,
        f"Привет {message.from_user.first_name}! Жми /registration или /login !",
    )


async def registration_pressed(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, UserStates.email, message.chat.id)
    await bot.send_message(message.chat.id, "Отправь свою почту")


async def process_email_step(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Придумай пароль")
    await bot.set_state(message.from_user.id, UserStates.password, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["email"] = message.text


async def process_password_step(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Укажи пол", reply_markup=kb_fem_or_male())
    await bot.set_state(message.from_user.id, UserStates.sex, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["password"] = message.text


async def process_sex_step(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id, "Введи через пробел возраст(в годах), вес(в кг), рост(в см)"
    )
    await bot.set_state(
        message.from_user.id, UserStates.age_weight_height, message.chat.id
    )
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["sex"] = message.text


async def process_age_weight_height_step(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id, "Выбери уровень активности:", reply_markup=kb_activity_lvls()
    )
    await bot.set_state(message.from_user.id, UserStates.activity_lvl, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["age"], data["weight"], data["height"] = [
            int(i) for i in message.text.split()
        ]


async def process_activity_lvl(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id, "Выбери цель:", reply_markup=kb_desired_result()
    )
    await bot.set_state(message.from_user.id, UserStates.desired_result, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["activity_lvl"] = activity[message.text]


async def process_desired_result(message: Message, bot: AsyncTeleBot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == "Похудение":
            data["desired_result"] = "weight loss"
        elif message.text == "Поддержка":
            data["desired_result"] = "support"
        else:
            data["desired_result"] = "mass gain"
        kcal = calorie_calculation(
            data["sex"],
            data["age"],
            data["weight"],
            data["height"],
            data["desired_result"],
            data["activity_lvl"],
        )

    await bot.send_message(
        message.chat.id,
        f"Рекомендуемое потребление калорий: {kcal}ккал, но можете записать свое значение",
        reply_markup=kb_daily_kcal(),
    )
    await bot.set_state(
        message.from_user.id, UserStates.newsletter, message.chat.id
    )


async def process_notify(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id, "Хотите получать уведомления?", reply_markup=kb_y_or_n()
    )
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["daily_kcal"] = message.text
    await bot.set_state(
        message.from_user.id, UserStates.id_tg, message.chat.id
    )


async def process_end_register(message: Message, bot: AsyncTeleBot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["newsletter"] = int(message.text == "Да")
        data["id_tg"] = message.chat.id
        await bot.send_message(message.chat.id, f"Вы успешно зарегестрировалсь {data}")
        
    await bot.delete_state(message.from_user.id, message.chat.id)



async def login_pressed(call: types.CallbackQuery, bot: AsyncTeleBot):
    await bot.send_message(chat_id=call.message.chat.id, text="Вход")


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()
