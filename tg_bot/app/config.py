from dotenv import dotenv_values

config = dotenv_values(".env")

REDIS_HOST = config.get("REDIS_HOST")
REDIS_PORT = int(config.get("REDIS_PORT"))
BOT_TOKEN = config.get("BOT_TOKEN")

db_host = config.get("db_host")
db_port = int(config.get("db_port"))

activity_lvls = [
    "Сидячий образ",
    "Умеренная активность",
    "Средняя активность",
    "Высокая активность",
    "Экстра активность",
]
activity = dict(zip(activity_lvls, [1.2, 1.375, 1.55, 1.725, 1.9]))
desired_result = {"Похудение": "weight loss", "Поддержка": "support", "Набор": "mass gain"}
db_url = f"http://{db_host}:{db_port}"
