"""
Модуль с инструментами

    Functions:
        calorie_calculation
        str_good
        str_to_int
        valid_date
        valid_int
        valid_mail
"""
import re
from datetime import datetime


def calorie_calculation(data):
    """Подсчитывает суточное потребление калорий по формудле Harris-Benedict Equation,
     где интенсивность метаболизма -  Basal Metabolic Rate (BMR)"""
    sex, age = data["sex"], data["age"]
    weight, height = data["weight"], data["height"]
    desired_result, activity_lvl = data["desired_result"], data["activity_lvl"]
    if sex:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    kcal = int(activity_lvl * bmr)
    if desired_result == "Поддержка":
        return kcal
    if desired_result == "Похудение":
        return int(kcal * 0.85)
    return int(kcal * 1.15)


def str_good(good: dict) -> str:
    """Пользовательское отображение продуктов"""
    nutritional_values = f"{good['kcal']}/{good['proteins']}/{good['fats']}/{good['carbohydrates']}"
    if not good['brand']:
        return f"{good['id']}: {good['name']}: " + nutritional_values
    return f"{good['id']}: {good['name']} {good['brand']}: " + nutritional_values


def str_to_int(s: str, count: int) -> list[int] | None:
    """Валидатор чисел, на вход подается строка чисел через пробел и их количество, вывыдит список чисел"""
    try:
        vals = [int(i) for i in s.split()]
    except ValueError:
        return
    if len(vals) != count or any([i < 0 for i in vals]):
        return
    return vals


def valid_date(date: str) -> str | None:
    """Функция проверяет дату и возвращает"""
    try:
        convert_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return
    return date


def valid_int(integer: str) -> int | None:
    """Функция проверяет строку на наличие числа в ней"""
    try:
        convert_int = int(integer)
    except ValueError:
        return
    return convert_int


def valid_mail(mail: str):
    """Валидация почты"""
    if re.match(r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$", mail):
        return mail
