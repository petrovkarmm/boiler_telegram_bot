import sqlite3

from db_configuration.db import get_connection


class User:
    @staticmethod
    def check_user_in_database(telegram_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM user WHERE telegram_id = ?", (telegram_id,))
            user = cursor.fetchone()

            if user is None:
                return False

            return True

    @staticmethod
    def add_user(
            telegram_id: str,
            telegram_first_name: str = None,
            telegram_last_name: str = None,
            telegram_username: str = None,
            name: str = None,
            organization_itn: str = None,
            organization_name: str = None,
            phone: str = None
    ):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO user (
                    telegram_id,
                    telegram_first_name,
                    telegram_last_name,
                    telegram_username,
                    name,
                    organization_itn,
                    organization_name,
                    phone
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                telegram_id,
                telegram_first_name,
                telegram_last_name,
                telegram_username,
                name,
                organization_itn,
                organization_name,
                phone
            ))

            conn.commit()

    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> dict | None:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row  # Позволяет получать строки как словари
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE telegram_id = ?", (telegram_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
