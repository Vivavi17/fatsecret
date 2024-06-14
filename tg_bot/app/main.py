import asyncio
from config import BOT_TOKEN
from telebot import asyncio_filters

from telebot.asyncio_storage import StateMemoryStorage
from models import UserStates
from telebot.async_telebot import AsyncTeleBot

from registration import (
    start_handler, process_end_register,
    registration_pressed,
    login_pressed, process_notify,
    process_email_step, process_desired_result,
    process_password_step, process_activity_lvl,
    process_sex_step, process_age_weight_height_step
)

bot = AsyncTeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())

@bot.message_handler(state="*", commands='cancel')
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Your state was cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)

def register_handlers():
    bot.register_message_handler(start_handler, commands=["start"], pass_bot=True)
    bot.register_message_handler(registration_pressed, commands="registration", pass_bot=True)
    bot.register_message_handler(
        process_email_step, state=UserStates.email, pass_bot=True
    )
    bot.register_message_handler(
        process_password_step, state=UserStates.password, pass_bot=True
    )
    bot.register_message_handler(process_sex_step, state=UserStates.sex, pass_bot=True)
    bot.register_message_handler(process_age_weight_height_step, state=UserStates.age_weight_height, pass_bot=True)
    bot.register_message_handler(process_activity_lvl, state=UserStates.activity_lvl, pass_bot=True)
    bot.register_message_handler(process_desired_result, state=UserStates.desired_result, pass_bot=True)
    bot.register_message_handler(process_notify, state=UserStates.newsletter, pass_bot=True)
    bot.register_message_handler(process_end_register, state=UserStates.newsletter, pass_bot=True)
    bot.register_callback_query_handler(
        login_pressed, func=lambda call: call.data == "login", pass_bot=True
    )


register_handlers()

bot.add_custom_filter(asyncio_filters.StateFilter(bot))


if __name__ == "__main__":
    asyncio.run(bot.polling(non_stop=True))  # restart_on_change=True
