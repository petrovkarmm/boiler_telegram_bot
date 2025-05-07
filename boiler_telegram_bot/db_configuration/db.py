from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "bot.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

