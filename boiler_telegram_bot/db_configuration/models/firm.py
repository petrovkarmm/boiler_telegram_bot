from boiler_telegram_bot.db_configuration.db_connection import get_connection


class Firm:
    @staticmethod
    def add_firm(user_id: int, firm_type: str) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Добавляем новую фирму
            cursor.execute("""
                INSERT INTO firm (user_id, firm_type)
                VALUES (?, ?, ?)
            """, (user_id, firm_type))

            conn.commit()
            return cursor.lastrowid
