import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = True

bot_token = os.getenv("BOT_TOKEN")
pyrus_login = os.getenv('PYRUS_LOGIN')
pyrus_security_key = os.getenv('PYRUS_SECURITY_KEY')
