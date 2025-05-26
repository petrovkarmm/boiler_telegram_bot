import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = False

redis_connect_url = os.getenv("REDIS_CONNECT_URL")
bot_token = os.getenv("BOT_TOKEN")
bot_test_token = os.getenv("BOT_TEST_TOKEN")
pyrus_login = os.getenv('PYRUS_LOGIN')
pyrus_security_key = os.getenv('PYRUS_SECURITY_KEY')
pyrus_standard_url = 'https://api.pyrus.com/v4'
admin_panel_password = os.getenv("ADMIN_PANEL_PASSWORD")

BOT_BASE_DIR = os.getcwd()
