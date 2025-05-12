import sqlite3

from db_configuration.db import get_connection


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
    def get_all_unviewed_feedback():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM feedback WHERE viewed = 0")
        results = cursor.fetchall()

        conn.close()
        return results

    @staticmethod
    def get_all_viewed_feedback():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
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

    @staticmethod
    def get_feedback_by_id(feedback_id: int):
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM feedback WHERE id = ?",
                       (feedback_id,))
        result = cursor.fetchone()

        conn.close()
        return result
