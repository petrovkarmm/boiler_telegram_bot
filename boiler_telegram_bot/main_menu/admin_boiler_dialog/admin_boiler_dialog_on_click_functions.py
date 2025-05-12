from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from db_configuration.models.feedback import Feedback
from main_menu.admin_boiler_dialog.admin_boiler_dialog_states import AdminBoilerDialog


async def go_to_boiler_bot(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(
        BoilerDialog.boiler_main_menu
    )


async def go_to_new_feedbacks(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['feedback_menu'] = 'new'
    await dialog_manager.switch_to(
        AdminBoilerDialog.admin_boiler_feedbacks_list
    )


async def go_to_old_feedbacks(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['feedback_menu'] = 'old'
    await dialog_manager.switch_to(
        AdminBoilerDialog.admin_boiler_feedbacks_list
    )


async def on_feedback_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        feedback_id: int,
):
    dialog_manager.dialog_data['feedback_id'] = feedback_id

    await dialog_manager.switch_to(
        AdminBoilerDialog.admin_boiler_feedback_view
    )


async def on_technical_problem_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        technical_problem_id: int,
):
    dialog_manager.dialog_data['technical_problem_id'] = technical_problem_id

    await dialog_manager.switch_to(
        AdminBoilerDialog.admin_boiler_technical_problem_view
    )


async def mark_feedback(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    feedback_id = dialog_manager.dialog_data['feedback_id']

    Feedback.mark_feedback_viewed(feedback_id=feedback_id)

    await dialog_manager.switch_to(
        AdminBoilerDialog.admin_boiler_feedbacks_list
    )
