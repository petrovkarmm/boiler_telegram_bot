from boiler_telegram_bot.db_configuration.db_connection import get_connection
from tg_logs.logger import bot_logger


def add_column_if_not_exists(table_name: str, column_name: str, column_type: str, default_value: str = None):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем список всех колонок в таблице
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]

    # Добавляем колонку, если её ещё нет
    if column_name not in columns:
        default_clause = f"DEFAULT {default_value}" if default_value is not None else ""
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} {default_clause}")
        conn.commit()

    conn.close()


if __name__ == "__main__":
    try:
        bot_logger.info('Ручная миграция.')

        # Добавим колонку is_individual — физлицо
        add_column_if_not_exists(
            table_name='user',
            column_name='have_individual',
            column_type='BOOLEAN',
            default_value='0'
        )
    except Exception as e:
        bot_logger.warning(e)
    else:
        bot_logger.info(
            'Ручная миграция прошла успешно.'
        )
