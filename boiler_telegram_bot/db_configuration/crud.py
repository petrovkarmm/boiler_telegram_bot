from db_configuration.db import get_connection


class User:
    @staticmethod
    def add_user_if_not_exists(telegram_id: int, name: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()

        if user is None:
            cursor.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
            conn.commit()

        conn.close()


class Feedback:
    @staticmethod
    def add_feedback(tg_user_id: int, firstname: str, lastname: str, username: str, text: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO feedback (tg_user_id, user_firstname, user_lastname, user_username, feedback_text)
        VALUES (?, ?, ?, ?, ?)
        """, (tg_user_id, firstname, lastname, username, text))

        conn.commit()
        conn.close()

    @staticmethod
    def get_unviewed_feedback():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM feedback WHERE viewed = 0")
        results = cursor.fetchall()

        conn.close()
        return results

    @staticmethod
    def get_viewed_feedback():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM feedback WHERE viewed = 1")
        results = cursor.fetchall()

        conn.close()
        return results

    @staticmethod
    def mark_feedback_viewed(feedback_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE feedback SET viewed = 1 WHERE id = ?", (feedback_id,))
        conn.commit()
        conn.close()
