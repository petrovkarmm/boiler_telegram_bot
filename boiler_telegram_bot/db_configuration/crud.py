import sqlite3

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


class TechnicalProblem:
    @staticmethod
    def get_all_technical_problem():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM technical_problem")
        results = cursor.fetchall()

        conn.close()
        return results

    @staticmethod
    def get_all_unhidden_technical_problem():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM technical_problem WHERE hidden = 0")
        results = cursor.fetchall()

        conn.close()
        return results

    @staticmethod
    def get_technical_problem_by_id(technical_problem_id: int):
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM technical_problem WHERE id = ?", (technical_problem_id,))
        result = cursor.fetchone()

        conn.close()
        return result

    @staticmethod
    def delete_technical_problem_by_id(technical_problem_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM technical_problem WHERE id = ?", (technical_problem_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def add_technical_problem(name: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO technical_problem (name, hidden)
        VALUES (?, ?)
        """, (name, 0))

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
                       (feedback_id, ))
        conn.commit()
        conn.close()
