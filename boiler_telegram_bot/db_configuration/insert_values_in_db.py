from boiler_telegram_bot.db_configuration.models.pyrus import PyrusToken
from boiler_telegram_bot.settings import pyrus_login, pyrus_security_key


def insert_values():
    PyrusToken.insert_login_data(pyrus_login=pyrus_login, pyrus_security_key=pyrus_security_key)

if __name__ == '__main__':
    insert_values()
