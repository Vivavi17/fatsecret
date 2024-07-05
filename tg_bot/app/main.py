"""
Модуль запуска бота и регистрации его ручек

    Classes:
        BotExceptionHandler

    Functions:
        del_any_state
        register_handlers_registration
        register_handlers_new_good
        register_handlers_add_note
        register_handlers_average_kcal
"""
import asyncio
import sys

from config import BOT_TOKEN
from telebot import asyncio_filters, types
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

sys.path.append(".")

from goods_handlers import (add_good, process_brand_step, process_name_step,
                            process_nutritional_values_step)
from journal_handlers import (add_note, find_average_kcal_period,
                              process_date_from_step, process_date_to_step,
                              process_goods_date_step,
                              process_goods_weight_step, process_id_goods_step,
                              process_name_goods_step)
from models import AddGoodStates, AverageKcalStates, GoodStates, UserStates
from registration_handlers import (process_activity_lvl_step,
                                   process_age_weight_height_step,
                                   process_desired_result_step, process_email_step,
                                   process_newsletter_step, process_daily_kcal_step,
                                   process_password_step, process_sex_step,
                                   registration)


class BotExceptionHandler:
    """Обработка ошибок"""
    def handle(self, error):
        raise error


bot = AsyncTeleBot(
    BOT_TOKEN, state_storage=StateMemoryStorage(), exception_handler=BotExceptionHandler()
)


@bot.message_handler(state="*", commands="cancel")
async def del_any_state(message):
    """Удаляет текущий статус процесса"""
    await bot.send_message(message.chat.id, "Процесс удален", reply_markup=types.ReplyKeyboardRemove())
    await bot.delete_state(message.from_user.id, message.chat.id)


def register_handlers_registration():
    """Подключает процесс для регистрации в боте"""
    bot.register_message_handler(
        registration, commands=["registration", "start"], pass_bot=True
    )
    bot.register_message_handler(
        process_email_step, state=UserStates.email, pass_bot=True
    )
    bot.register_message_handler(
        process_password_step, state=UserStates.password, pass_bot=True
    )
    bot.register_message_handler(process_sex_step, state=UserStates.sex, pass_bot=True)
    bot.register_message_handler(
        process_age_weight_height_step,
        state=UserStates.age_weight_height,
        pass_bot=True,
    )
    bot.register_message_handler(
        process_activity_lvl_step, state=UserStates.activity_lvl, pass_bot=True
    )
    bot.register_message_handler(
        process_desired_result_step, state=UserStates.desired_result, pass_bot=True
    )
    bot.register_message_handler(
        process_daily_kcal_step, state=UserStates.daily_kcal, pass_bot=True
    )
    bot.register_message_handler(
        process_newsletter_step, state=UserStates.newsletter, pass_bot=True
    )


def register_handlers_new_good():
    """Подключает процесс для добавления нового продукта"""
    bot.register_message_handler(add_good, commands=["new_good"], pass_bot=True)
    bot.register_message_handler(
        process_name_step, state=AddGoodStates.name, pass_bot=True
    )
    bot.register_message_handler(
        process_brand_step, state=AddGoodStates.brand, pass_bot=True
    )
    bot.register_message_handler(
        process_nutritional_values_step, state=AddGoodStates.nutritional_values, pass_bot=True
    )


def register_handlers_add_note():
    """Подключает процесс для добавления записи в журнал"""
    bot.register_message_handler(add_note, commands=["add_note"], pass_bot=True)
    bot.register_message_handler(
        process_name_goods_step, state=GoodStates.name, pass_bot=True
    )
    bot.register_message_handler(
        process_id_goods_step, state=GoodStates.id, pass_bot=True
    )
    bot.register_message_handler(
        process_goods_weight_step, state=GoodStates.weight, pass_bot=True
    )
    bot.register_message_handler(
        process_goods_date_step, state=GoodStates.date, pass_bot=True
    )


def register_handlers_average_kcal():
    """Подключает процесс подсчета средних показателей КБЖУ за период"""
    bot.register_message_handler(find_average_kcal_period, commands=["average_kcal"], pass_bot=True)
    bot.register_message_handler(
        process_date_from_step, state=AverageKcalStates.date_from, pass_bot=True
    )
    bot.register_message_handler(
        process_date_to_step, state=AverageKcalStates.date_to, pass_bot=True
    )


if __name__ == "__main__":
    register_handlers_registration()
    register_handlers_new_good()
    register_handlers_add_note()
    register_handlers_average_kcal()
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))

    asyncio.run(bot.polling(non_stop=True))  # restart_on_change=True
