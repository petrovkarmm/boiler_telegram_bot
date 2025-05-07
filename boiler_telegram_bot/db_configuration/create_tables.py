from db_configuration.db import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technical_problem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        hidden BOOLEAN DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_user_id INTEGER,
        user_firstname TEXT,
        user_lastname TEXT,
        user_username TEXT,
        feedback_text TEXT,
        viewed BOOLEAN DEFAULT 0,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
