import os
import tempfile
import time

from boiler_telegram_bot.tg_logs.logger import bot_logger

TMP_DIR = tempfile.gettempdir()
EXPIRATION_DAYS = 30


def get_file_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


async def cleanup_tmp_files():
    now = time.time()
    expiration_time = now - 7 * 24 * 60 * 60

    all_files = [f for f in os.listdir(TMP_DIR) if os.path.isfile(os.path.join(TMP_DIR, f))]
    bot_logger.info(f"[CLEANUP] Все файлы в TMP: {', '.join(all_files) if all_files else 'Папка пуста'}")

    total_deleted = 0
    total_size_mb = 0.0

    for filename in os.listdir(TMP_DIR):
        file_path = os.path.join(TMP_DIR, filename)

        if not os.path.isfile(file_path):
            continue

        try:
            created = os.path.getctime(file_path)
            if created < expiration_time:
                file_size_mb = get_file_size_mb(file_path)
                os.remove(file_path)
                total_deleted += 1
                total_size_mb += file_size_mb
        except Exception as e:
            bot_logger.exception(f"Ошибка при попытке удалить файл {file_path}: {e}")

    if total_deleted > 0:
        bot_logger.info(
            f"[CLEANUP] Удалено файлов: {total_deleted}, Освобождено: {total_size_mb:.2f} MB"
        )
    else:
        bot_logger.info("[CLEANUP] Нет устаревших файлов для удаления.")
