import asyncio
import random
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, BaseDialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, ManagedCounter
from aiogram.exceptions import TelegramRetryAfter

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from db_configuration.crud import Feedback, TechnicalProblem


async def send_feedback(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_answer = dialog_manager.dialog_data.get('user_answer', 'ERROR')

    tg_user_id = callback.from_user.id
    user_username = '@' + callback.from_user.username
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name

    Feedback.add_feedback(
        tg_user_id=tg_user_id,
        firstname=user_first_name,
        lastname=user_last_name,
        username=user_username,
        text=user_answer
    )

    await callback.message.answer(
        text='Спасибо, что помогаете нам стать лучше!'
    )

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    await dialog_manager.switch_to(
        BoilerDialog.boiler_main_menu
    )


async def on_technical_problem_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        technical_problem_id_selected: int,
):
    technical_problem = TechnicalProblem.get_technical_problem_by_id(
        technical_problem_id=technical_problem_id_selected
    )

    if technical_problem:
        dialog_manager.dialog_data['technical_problem'] = technical_problem['name']
        await dialog_manager.switch_to(
            BoilerDialog.boiler_repair_description
        )
    else:
        await callback.message.answer(
            text='Кажется, что-то пошло не так. . .\n\n'
                 'Попробуйте ещё раз.'
        )
        await dialog_manager.switch_to(
            BoilerDialog.boiler_main_menu
        )
