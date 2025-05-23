import logging
import time
from functools import wraps
from logging.handlers import TimedRotatingFileHandler

from settings import BOT_BASE_DIR

bot_logger = logging.getLogger('bot_logger')
bot_logger.setLevel(logging.INFO)
bot_file_handler = TimedRotatingFileHandler(
    f'{BOT_BASE_DIR}/tg_logs/aiogram.log',
    when='W0',
    interval=1,
    backupCount=4,
    encoding='utf-8'
)
bot_file_handler.setLevel(logging.INFO)
bot_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
bot_file_handler.setFormatter(bot_formatter)
bot_logger.addHandler(bot_file_handler)

logging.getLogger('aiogram').setLevel(logging.WARNING)


async def handler_log(user, state, start_data, dialog_data):
    log_message = (
        f"Состояние: {state} | start_data: {start_data} | dialog_data: {dialog_data}User: {user} |"
    )
    bot_logger.info(log_message)


def log_async_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        log_message = f"Вызов запроса: {func.__name__} | Аргументы: {args} | Каргументы: {kwargs}"
        bot_logger.info(log_message)

        start_time = time.time()
        try:
            result = await func(*args, **kwargs)

            if isinstance(result, tuple) and len(result) == 2:
                status_code, response = result
                bot_logger.info(f"Окончание запроса: {func.__name__} | Статус код: {status_code} | "
                                f"Ответ: {response}")
            else:
                bot_logger.info(f"Окончание запроса: {func.__name__} | Ответ: {result}")

            execution_time = time.time() - start_time
            bot_logger.info(f"Время ожидания: {execution_time:.4f} секунд")

            return result
        except Exception as e:
            bot_logger.error(f"Ошибка в запросе: {func.__name__}\n{e}", exc_info=True)
            raise e

    return wrapper
