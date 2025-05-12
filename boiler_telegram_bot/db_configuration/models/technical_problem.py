import sqlite3

from db_configuration.db import get_connection


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
    def toggle_hidden_by_id(technical_problem_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE technical_problem
            SET hidden = NOT hidden,
                updated = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (technical_problem_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def delete_technical_problem_by_id(technical_problem_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM technical_problem WHERE id = ?", (technical_problem_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def add_technical_problem(name: str, hidden: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO technical_problem (name, hidden)
        VALUES (?, ?)
        """, (name, hidden))

        conn.commit()
        conn.close()
