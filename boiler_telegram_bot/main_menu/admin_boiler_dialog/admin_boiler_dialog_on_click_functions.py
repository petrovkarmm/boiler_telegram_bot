from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog


async def go_to_boiler_bot(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(
        BoilerDialog.boiler_main_menu
    )



async def on_new_feedback_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        new_feedback_id: int,
):
    pass