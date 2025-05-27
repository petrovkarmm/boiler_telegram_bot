from boiler_telegram_bot.db_configuration.db_connection import get_connection


class Firm:
    @staticmethod
    def add_firm(user_id: int, firm_type: str) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Проверяем, есть ли у пользователя хотя бы одна фирма
            cursor.execute("SELECT COUNT(*) FROM firm WHERE user_id = ?", (user_id,))
            firm_count = cursor.fetchone()[0]

            is_main = 1 if firm_count == 0 else 0

            # Добавляем новую фирму
            cursor.execute("""
                INSERT INTO firm (user_id, firm_type, is_main)
                VALUES (?, ?, ?)
            """, (user_id, firm_type, is_main))

            conn.commit()
            return cursor.lastrowid
