from db_configuration.db import get_connection


#  TODO rename
class PyrusToken:
    @staticmethod
    def get_token() -> str | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT access_token FROM pyrus_token LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else None

    @staticmethod
    def get_login_data() -> tuple[str, str] | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pyrus_login, pyrus_security_key FROM pyrus_token LIMIT 1")
            row = cursor.fetchone()
            return (row[0], row[1]) if row else None

    @staticmethod
    def update_token(old_token: str, new_token: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pyrus_token SET access_token = ?, updated = CURRENT_TIMESTAMP WHERE access_token = ?",
                (new_token, old_token)
            )

    @staticmethod
    def insert_login_data(pyrus_login: str, pyrus_security_key: str):
        with get_connection() as conn:
            cursor = conn.cursor()

            # Проверка на существование
            cursor.execute("""
                SELECT id FROM pyrus_token WHERE pyrus_security_key = ?
            """, (pyrus_security_key,))
            existing = cursor.fetchone()

            if existing:
                print("Запись с таким security_key уже существует. Пропускаем вставку.")
                return

            cursor.execute("""
                INSERT INTO pyrus_token (pyrus_login, pyrus_security_key)
                VALUES (?, ?)
            """, (pyrus_login, pyrus_security_key))
