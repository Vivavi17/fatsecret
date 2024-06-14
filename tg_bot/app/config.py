BOT_TOKEN = "7375682689:AAGFPDcdgwJw4yjEJHsc5AETt_OPZrbodtI"

REDIS_PORT = 6379
REDIS_HOST = "localhost"
activity_lvls = [
    "Сидячий образ",
    "Умеренная активность",
    "Средняя активность",
    "Высокая активность",
    "Экстра активность",
]
activity = dict(zip(activity_lvls, [1.2, 1.375, 1.55, 1.725, 1.9]))
