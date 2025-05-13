import asyncio
import random
from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, BaseDialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, ManagedCounter
from aiogram.exceptions import TelegramRetryAfter

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from db_configuration.models.technical_problem import TechnicalProblem
from db_configuration.models.feedback import Feedback


async def get_barista_count_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    barista_counter: ManagedCounter = dialog_manager.find('barista_counter')

    barista_value = barista_counter.get_value()  # int число от 1 до 24
    dialog_manager.dialog_data['barista_value'] = barista_value
    #  TODO в окно итоговое


async def confirm_sending_call_technician(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_name = dialog_manager.dialog_data['user_name']
    technical_problem = dialog_manager.dialog_data['technical_problem']
    technical_problem_description = dialog_manager.dialog_data['technical_problem_description']
    user_phone = dialog_manager.dialog_data['user_phone']
    media_info = 'Медиа отсутствует.'

    #  TODO интеграция с CRM системой.

    await callback.message.answer(
        text=(
            "<b>📤 Имитируем отправку в CRM систему...</b>\n\n"
            f"👤 <b>Имя пользователя:</b> {user_name}\n"
            f"📞 <b>Телефон:</b> {user_phone}\n"
            f"🛠 <b>Описание проблемы:</b> {technical_problem_description}\n"
            f"⚙️ <b>Тип проблемы:</b> {technical_problem}\n"
            f"🖼 <b>Медиа:</b> {media_info}"
        ),
        parse_mode=ParseMode.HTML
    )

    await callback.message.answer(
        text="✅ <b>Заявка успешно принята!</b>\n📞 Ожидайте звонка.",
        parse_mode=ParseMode.HTML
    )

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    await dialog_manager.switch_to(
        BoilerDialog.boiler_main_menu
    )


async def send_feedback(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_answer = dialog_manager.dialog_data.get('user_answer', 'ERROR')

    tg_user_id = callback.from_user.id
    user_username = callback.from_user.username
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name

    if user_username:
        user_username = '@' + user_username
    else:
        user_username = 'Username отсутствует'

    if not user_first_name:
        user_first_name = 'Имя отсутствует'

    if not user_last_name:
        user_last_name = 'Фамилия отсутствует'

    Feedback.add_feedback(
        tg_user_id=tg_user_id,
        firstname=user_first_name,
        lastname=user_last_name,
        username=user_username,
        text=user_answer
    )

    await callback.message.answer(
        text=(
            "🙏 <b>Спасибо, что помогаете нам стать лучше!</b>\n\n"
            "Ваш отзыв очень важен для нас 💬\n"
            "Мы ценим ваше время и поддержку! 🌟"
        ),
        parse_mode=ParseMode.HTML
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
            text=(
                "❌ <b>Кажется, что-то пошло не так...</b>\n\n"
                "Пожалуйста, попробуйте ещё раз 🔄\n"
                "Если проблема не исчезнет, сообщите нам! 💬"
            ),
            parse_mode=ParseMode.HTML
        )
        await dialog_manager.switch_to(
            BoilerDialog.boiler_main_menu
        )
