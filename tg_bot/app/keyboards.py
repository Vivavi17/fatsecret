from telebot import types
from config import activity_lvls


def kb_fem_or_male():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Мужской", "Женский")
    return markup


def kb_activity_lvls():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*activity_lvls)
    return markup


def kb_desired_result():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Похудение", "Поддержка", "Набор")
    return markup


def kb_daily_kcal():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Оставить текущее значение")
    return markup


def kb_y_or_n():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Да", "Нет")
    return markup
