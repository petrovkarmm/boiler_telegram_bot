import sqlite3

from boiler_telegram_bot.db_configuration.db_connection import get_connection


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
    def get_user_by_telegram_id(telegram_id: str):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user WHERE telegram_id = ?", (telegram_id,))

            result = cursor.fetchone()

            return result

    @staticmethod
    def update_user_field(telegram_id: str,
                          key: str,
                          new_value: str = None):
        # Проверка допустимых полей для безопасности
        allowed_fields = {
            "name", "phone", "organization_itn", "organization_name"
        }

        if key not in allowed_fields:
            raise ValueError(f"Недопустимое поле: {key}")

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"""
                UPDATE user
                SET {key} = ?
                WHERE telegram_id = ?
                """,
                (new_value, telegram_id)
            )

            conn.commit()
