import asyncio
import random
from pprint import pprint
from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, ManagedCounter, ManagedRadio

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from db_configuration.models.technical_problem import TechnicalProblem
from db_configuration.models.feedback import Feedback
from db_configuration.models.user import User
from main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog


async def get_barista_count_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    barista_counter: ManagedCounter = dialog_manager.find('barista_counter')

    barista_value = barista_counter.get_value()  # int число от 1 до 24
    dialog_manager.dialog_data['barista_value'] = barista_value
    await dialog_manager.switch_to(
        BoilerDialog.boiler_barista_training_accept_request
    )


async def save_rent_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['button_click'] = 'Аренда'
    await dialog_manager.switch_to(
        BoilerDialog.boiler_rent
    )


async def rent_radio_set(
        event: CallbackQuery,
        widget: ManagedRadio,
        dialog_manager: DialogManager,
        item_id: Any,

):
    dialog_manager.dialog_data['radio_get_set'] = True


async def save_tech_cat_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['button_click'] = 'Подбор техники'
    await dialog_manager.switch_to(
        BoilerDialog.boiler_technical_catalog_type_choose
    )


async def save_barista_training_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['button_click'] = 'Обучение бариста'
    await dialog_manager.switch_to(
        BoilerDialog.boiler_barista_training_choose_count
    )


async def confirm_sending_call_technician(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_id = str(callback.from_user.id)

    user_data = User.get_user_by_telegram_id(
        user_id
    )

    if user_data:
        user_phone = user_data['phone']
        user_name = user_data['name']
        organization_itn = user_data['organization_itn']
        organization_name = user_data['organization_name']

        technical_problem = dialog_manager.dialog_data['technical_problem']
        technical_problem_description = dialog_manager.dialog_data['technical_problem_description']
        user_address = dialog_manager.dialog_data['user_address']
        media_info = 'Медиа отсутствует.'

        #  TODO интеграция с CRM системой.

        await callback.message.answer(
            text=(
                "<b>📤 Имитируем отправку в CRM систему...</b>\n\n"
                f"👤 <b>Имя пользователя:</b> {user_name}\n"
                f"📞 <b>Телефон:</b> {user_phone}\n"
                f"🛠 <b>Описание проблемы:</b> {technical_problem_description}\n"
                f"⚙️ <b>Тип проблемы:</b> {technical_problem}\n"
                f'🏘 <b>Адрес:</b> {user_address}\n'
                f"🏢 <b>Организация:</b> {organization_name}\n"
                f"🧾 <b>ИНН:</b> {organization_itn}\n"
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

    else:
        await dialog_manager.start(
            BoilerRegistrationDialog.boiler_registration_user_name
        )


async def confirm_sending_rent_request(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_id = str(callback.from_user.id)
    user_data = User.get_user_by_telegram_id(user_id)

    if user_data:
        request_title = dialog_manager.dialog_data['button_click']

        user_name = user_data['name']
        user_phone = user_data['phone']
        organization_itn = user_data['organization_itn']
        organization_name = user_data['organization_name']

        user_address = dialog_manager.dialog_data.get('user_address', '—')
        user_budget = dialog_manager.dialog_data.get('user_budget', '—')
        place_format = dialog_manager.dialog_data.get('place_format', '—')
        user_rent_type = dialog_manager.dialog_data.get('user_rent_type', '—')

        # TODO: Интеграция с CRM системой.

        await callback.message.answer(
            text=(
                "<b>📤 Имитируем отправку в CRM систему...</b>\n\n"
                f"🔗 <b>Название секции:</b> {request_title}\n"
                f"👤 <b>Имя пользователя:</b> {user_name}\n"
                f"📞 <b>Телефон:</b> {user_phone}\n"
                f"🏢 <b>Организация:</b> {organization_name}\n"
                f"🧾 <b>ИНН:</b> {organization_itn}\n"
                f"📍 <b>Адрес:</b> {user_address}\n"
                f"🏷 <b>Тип аренды:</b> {user_rent_type}\n"
                f"💰 <b>Бюджет:</b> {user_budget}\n"
                f"🏬 <b>Формат заведения:</b> {place_format}"
            ),
            parse_mode=ParseMode.HTML
        )

        await callback.message.answer(
            text="✅ <b>Заявка на аренду успешно отправлена!</b>\n📞 Мы с вами свяжемся в ближайшее время.",
            parse_mode=ParseMode.HTML
        )

        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
        await dialog_manager.switch_to(BoilerDialog.boiler_main_menu)

    else:
        await dialog_manager.start(BoilerRegistrationDialog.boiler_registration_user_name)


async def confirm_sending_barista_training(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_id = str(callback.from_user.id)

    user_data = User.get_user_by_telegram_id(
        user_id
    )

    if user_data:
        request_title = dialog_manager.dialog_data['button_click']
        barista_value = dialog_manager.dialog_data['barista_value']
        user_phone = user_data['phone']
        user_name = user_data['name']
        organization_itn = user_data['organization_itn']
        organization_name = user_data['organization_name']

        await callback.message.answer(
            text=(
                "<b>📤 Имитируем отправку в CRM систему...</b>\n\n"
                f"🔗 <b>Название секции:</b> {request_title}\n"
                f"👤 <b>Имя пользователя:</b> {user_name}\n"
                f'📌 <b>Кол-во человек на обучение:</b> {barista_value}\n'
                f'📞 <b>Телефон:</b> {user_phone}\n'
                f"🏢 <b>Организация:</b> {organization_name}\n"
                f"🧾 <b>ИНН:</b> {organization_itn}\n"

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


    else:
        await dialog_manager.start(
            BoilerRegistrationDialog.boiler_registration_user_name
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
