def calorie_calculation(sex, age, weight, height, desired_result, activity_lvl):
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
