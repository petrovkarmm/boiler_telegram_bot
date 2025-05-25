import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'bot.db')


def get_connection():
    return sqlite3.connect(DB_PATH)
