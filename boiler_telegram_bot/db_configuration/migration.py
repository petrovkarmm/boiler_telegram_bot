from boiler_telegram_bot.db_configuration.db_connection import get_connection
from tg_logs.logger import bot_logger


def migrate_user_decomposition():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Новая таблица user_new
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        telegram_first_name TEXT,
        telegram_last_name TEXT,
        telegram_username TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Таблица firm с фиксами
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        firm_type TEXT NOT NULL CHECK (firm_type IN ('legal_entity', 'individual')),
        is_main BOOLEAN NOT NULL CHECK (is_main IN (0, 1)) DEFAULT 0,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. firm_info_legal_entity
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firm_info_legal_entity (
        firm_id INTEGER PRIMARY KEY,
        organization_name TEXT,
        organization_representative_name TEXT,
        organization_itn TEXT,
        phone TEXT,
        FOREIGN KEY (firm_id) REFERENCES firm(id)
    )
    """)

    # 4. firm_info_individual (на будущее)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firm_info_individual (
        firm_id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        FOREIGN KEY (firm_id) REFERENCES firm(id)
    )
    """)

    # 5. Чтение старых данных
    cursor.execute("""
    SELECT id, telegram_id, telegram_first_name, telegram_last_name, telegram_username,
           name, phone, organization_itn, organization_name,
           created, updated
    FROM user
    """)
    rows = cursor.fetchall()

    for row in rows:
        (user_id, telegram_id, first_name, last_name, username,
         rep_name, phone, itn, org_name, created, updated) = row

        # user_new
        cursor.execute("""
        INSERT INTO user_new (id, telegram_id, telegram_first_name, telegram_last_name, telegram_username, created, updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, telegram_id, first_name, last_name, username, created, updated))

        # firm
        cursor.execute("""
        INSERT INTO firm (user_id, firm_type, is_main)
        VALUES (?, 'legal_entity', 1)
        """, (user_id,))
        firm_id = cursor.lastrowid

        # firm_info_legal_entity
        cursor.execute("""
        INSERT INTO firm_info_legal_entity (firm_id, organization_name, organization_representative_name, organization_itn, phone)
        VALUES (?, ?, ?, ?, ?)
        """, (firm_id, org_name, rep_name, itn, phone))

    # Удаляем старую таблицу user
    cursor.execute("DROP TABLE user")

    # Переименовываем user_new → user
    cursor.execute("ALTER TABLE user_new RENAME TO user")

    conn.commit()
    conn.close()
    print(f"Migration completed successfully. Migrated {len(rows)} users.")
