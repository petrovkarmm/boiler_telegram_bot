import sqlite3

from boiler_telegram_bot.db_configuration.db_connection import get_connection


class TechnicalProblem:
    @staticmethod
    def get_all_technical_problem():
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM technical_problem")
            results = cursor.fetchall()

            return results

    @staticmethod
    def get_all_unhidden_technical_problem():
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM technical_problem WHERE hidden = 0")
            results = cursor.fetchall()

            return results

    @staticmethod
    def get_technical_problem_by_id(technical_problem_id: int):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM technical_problem WHERE id = ?", (technical_problem_id,))
            result = cursor.fetchone()

            return result

    @staticmethod
    def toggle_hidden_by_id(technical_problem_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE technical_problem
                SET hidden = NOT hidden,
                    updated = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (technical_problem_id,))

            conn.commit()

    @staticmethod
    def delete_technical_problem_by_id(technical_problem_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM technical_problem WHERE id = ?", (technical_problem_id,))
            conn.commit()

    @staticmethod
    def add_technical_problem(name: str, hidden: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO technical_problem (name, hidden)
            VALUES (?, ?)
            """, (name, hidden))

            conn.commit()
