from telebot.asyncio_handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    email = State()
    password = State()
    sex = State()
    age_weight_height = State()
    desired_result = State()
    activity_lvl = State()
    daily_kcal = State()
    newsletter = State()
    id_tg = State()
    
