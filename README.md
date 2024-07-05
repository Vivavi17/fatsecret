# Fatsecret TG-bot

Приложение для отслеживания калорий.
  

### Установка зависимостей

	pip3 install -r backend/requirements.txt
    pip3 install -r tg_bot/requirements.txt


### Запуск API

	alembic upgrade head
	python3 backend/app/main.py

### Запуск TG-bot

	python3 tg_bot/app/main.py

###  Структура дерева директорий

	fatsecret
	├── backend
	│ └── app
	│ ├── dao
	│ ├── goods
	│ ├── journal
	│ ├── migrations
	│ │ └── versions
	│ └── users
	└── tg_bot
	└── app

  
### Описание модулей

**base.py**
Интерфейс DAO с описанием общих методов классов взаимодействия с БД
**dao.py**
Интерфейсы по работе с определенными таблицами в БД
 **model.py**
Модули SQLalchemy-моделей отбражающие таблицы в БД
**schemas.py**
Модули с pydantic-моделями
**service.py**
Модули бизнес-логики
**depends.py**
Модуль pydantic-зависимостей
**cache.py**
Модуль конфигурации redis
**config.py**
Модуль Pydantic Settings для переменных окружения
**datebase.py**
Модуль конфигурации БД
**exceptions.py**
Модуль с собственными HTTP-исключениями
**main.py**
Модуль конфигурации FastAPI
**router.py**
Модули с набором ручек

 - **goods**
	 - /goods - поиск продуктов по названию
	 - /goods - добавление продуктов
	- /goods/{product_id} - обновление информции
- **journal**
	 - /journal/{user_id} - добавить запись
	- /journal/{user_id}/{date_from}-{date_to} - получить среднее дневное КБЖУ  
- **users**
	- /auth/register - регистрация пользователя
	- /auth/login - вход в учетную запись
	 - /auth/logout - выход
	- /auth/refresh - обновить токены доступа
	- /auth/ping_me - посмотреть текужего пользователя
