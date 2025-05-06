import asyncio
import random

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, BaseDialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, ManagedCounter
from aiogram.exceptions import TelegramRetryAfter

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog


async def send_feedback(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_answer = dialog_manager.dialog_data.get('user_answer', 'ERROR')

    user_id = callback.from_user.id
    user_username = callback.from_user.username
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name

    await callback.message.answer(
        text=f'-------------------------\n'
             f'Передаём в CRM систему фидбек пользователя: {user_answer}\n\n'
             f'Данные пользователя:\n\n'
             f'TG ID: {user_id}\n'
             f'Username: @{user_username}\n'
             f'Имя: {user_first_name}\n'
             f'Фамилия: {user_last_name}\n'
             f'-------------------------'
    )

    await callback.message.answer(
        text='Спасибо, что помогаете нам стать лучше!'
    )

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    await dialog_manager.switch_to(
        BoilerDialog.boiler_main_menu
    )
