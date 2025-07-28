# boiler_telegram_bot Заказ для https://boiler-serv.ru/.

env:

BOT_TOKEN=

BOT_TEST_TOKEN= 

PYRUS_SECURITY_KEY=

PYRUS_LOGIN=

REDIS_CONNECT_URL=

REDIS_PASSWORD=

ADMIN_PANEL_PASSWORD=

Любая директория, работает load_dotenv(find_dotenv())

Запуск проекта - стандартное поднятие докер-компоуза.

*При debug True в settings убирается redis, запуск через файл bot.py с созданием таблиц вручную (
db_configurtaion/create_table + insert_values_in_db))
