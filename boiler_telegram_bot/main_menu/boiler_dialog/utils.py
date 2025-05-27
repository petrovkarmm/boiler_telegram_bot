import re
import aiohttp
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


async def download_file(bot: Bot, file_id: str, message: Message) -> bytes | None:
    try:
        file_info = await bot.get_file(file_id)
    except TelegramBadRequest as e:
        if "file is too big" in str(e).lower():
            await message.answer("Файл слишком большой. Telegram не позволяет его скачать.")
        else:
            await message.answer(f"Произошла ошибка: {str(e)}")
        return None

    if file_info.file_size > MAX_FILE_SIZE:
        await message.answer("Файл слишком большой. Максимальный размер — 20 МБ.")
        return None

    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status == 200:
                return await resp.read()
            await message.answer("Не удалось скачать файл. Попробуйте позже.")
            return None


async def normalize_phone_number(phone: str) -> str | None:
    digits = re.sub(r"\D", "", phone)

    if len(digits) != 11:
        return None

    if digits.startswith("8") or digits.startswith("7"):
        return "+7" + digits[1:]
    elif digits.startswith("9"):
        return "+7" + digits
    else:
        return None


end_states_title = {'Подбор техники': BoilerDialog.boiler_accept_tech_cat_request,
                    'Обучение бариста': BoilerDialog.boiler_barista_training_accept_request,
                    'Аренда': BoilerDialog.boiler_rent_accept_request,
                    'Вызов техника': BoilerDialog.boiler_repair_accept_request
                    }
