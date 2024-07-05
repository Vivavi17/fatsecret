"""
Модуль содержит клавиатуры бота

    Functions -> markup:
        kb_fem_or_male
        kb_activity_lvls
        kb_desired_result
        kb_daily_kcal
        kb_y_or_n
        kb_list_goods
        kb_date
        kb_no_brand
"""
from datetime import date

from config import activity_lvls
from telebot import types

from app.utils import str_good


def kb_fem_or_male():
    """Клавиатура выбора пола юзера"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Мужской", "Женский")
    return markup


def kb_activity_lvls():
    """Клавиатура выбора активности пользователя"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*activity_lvls)
    return markup


def kb_desired_result():
    """Клавиатура выбора цели пользователя"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Похудение", "Поддержка", "Набор")
    return markup


def kb_daily_kcal(kcal):
    """Кнопка с расчитаной калорийностью"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(kcal)
    return markup


def kb_y_or_n():
    """Клавиатура соглашения"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Да", "Нет")
    return markup


def kb_list_goods(goods):
    """Клавиатура для выбора найденных продуктов"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(*[str_good(i) for i in goods])
    return markup


def kb_date():
    """Кнопа с текущей датой"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(str(date.today()))
    return markup


def kb_no_brand():
    """Кнопка для неопределенного бренда продуктов"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Без бренда")
    return markup
