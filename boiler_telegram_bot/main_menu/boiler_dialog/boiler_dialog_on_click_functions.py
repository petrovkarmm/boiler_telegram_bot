from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, ManagedCounter, ManagedRadio

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from boiler_telegram_bot.db_configuration.models.feedback import Feedback
from boiler_telegram_bot.db_configuration.models.technical_problem import TechnicalProblem
from boiler_telegram_bot.db_configuration.models.user import User
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_dataclasses import TECHNICAL_CATALOG, RENT_TYPE
from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog
from boiler_telegram_bot.pyrus_api.pyrus_utils import send_form_task
from boiler_telegram_bot.main_menu.boiler_dialog.utils import end_states_title, previous_states_title
from boiler_telegram_bot.db_configuration.models.firm import Firm


async def get_barista_count_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    barista_counter: ManagedCounter = dialog_manager.find('barista_counter')

    barista_value = barista_counter.get_value()
    dialog_manager.dialog_data['barista_value'] = barista_value
    await dialog_manager.switch_to(
        BoilerDialog.boiler_profile_choose
    )


async def go_to_previous_state_from_profile_choosing(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    button_click = dialog_manager.dialog_data['button_click']

    previous = previous_states_title.get(button_click)

    await dialog_manager.switch_to(
        previous
    )


async def go_to_profile_rent_accepting_request(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    rent_radio_rent_type_widget = dialog_manager.find(
        'rent_type'
    )
    rent_radio_catalog_widget = dialog_manager.find(
        'rent_tech_type'
    )

    rent_radio_rent_type_widget: ManagedRadio
    rent_radio_catalog_widget: ManagedRadio

    user_rent_type = RENT_TYPE.get(rent_radio_rent_type_widget.get_checked(), 'ERROR')
    user_technical_type = TECHNICAL_CATALOG.get(rent_radio_catalog_widget.get_checked(), 'ERROR')

    dialog_manager.dialog_data['user_rent_type'] = user_rent_type
    dialog_manager.dialog_data['user_technical_type'] = user_technical_type

    await dialog_manager.switch_to(
        BoilerDialog.boiler_profile_choose
    )


async def on_profile_selected(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        profile_id: int,
):
    button_click = dialog_manager.dialog_data['button_click']

    firm_data = Firm.get_firm_info_by_id(profile_id)

    if firm_data:

        if firm_data['firm_type'] == 'legal_entity':
            dialog_manager.dialog_data['firm_type'] = firm_data['firm_type']
            dialog_manager.dialog_data['user_name'] = firm_data['representative_name']
            dialog_manager.dialog_data['organization_itn'] = firm_data['itn']
            dialog_manager.dialog_data['organization_name'] = firm_data['organization_name']
            dialog_manager.dialog_data['user_phone'] = firm_data['phone']

        if firm_data['firm_type'] == 'individual':
            dialog_manager.dialog_data['firm_type'] = firm_data['firm_type']
            dialog_manager.dialog_data['user_name'] = firm_data['name']
            dialog_manager.dialog_data['user_phone'] = firm_data['phone']

        next_state = end_states_title.get(button_click)

        await dialog_manager.switch_to(
            next_state
        )

    else:

        await dialog_manager.start(
            BoilerRegistrationDialog.boiler_registration_user_name
        )


async def technical_catalog_radio_set(
        event: CallbackQuery,
        widget: ManagedRadio,
        dialog_manager: DialogManager,
        item_id: Any,

):
    dialog_manager.dialog_data['technical_catalog_radio_get_set'] = True


async def rent_radio_set(
        event: CallbackQuery,
        widget: ManagedRadio,
        dialog_manager: DialogManager,
        item_id: Any,

):
    dialog_manager.dialog_data['rent_type_radio_get_set'] = True


async def rent_catalog_radio_set(
        event: CallbackQuery,
        widget: ManagedRadio,
        dialog_manager: DialogManager,
        item_id: Any,

):
    dialog_manager.dialog_data['rent_catalog_radio_get_set'] = True


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


async def save_repair_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['button_click'] = 'Вызов техника'
    await dialog_manager.switch_to(
        BoilerDialog.boiler_repair_problem
    )


async def save_rent_and_switch(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['button_click'] = 'Аренда'
    await dialog_manager.switch_to(
        BoilerDialog.boiler_rent_type
    )


async def confirm_sending_call_technician(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    # TODO изменить логику под фл/юр лиц.
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

        filename = dialog_manager.dialog_data['filename']
        tmp_file_path = dialog_manager.dialog_data['tmp_file_path']

        task_description = (f"\n"
                            f"Описание проблемы: {technical_problem_description}\n\n")

        await send_form_task(
            callback=callback,
            user_name=user_name,
            user_phone=user_phone,
            user_address=user_address,
            task_title=technical_problem,
            task_description=task_description,
            dialog_manager=dialog_manager,
            filename=filename,
            tmp_file_path=tmp_file_path,
            organization_name=organization_name,
            organization_itn=organization_itn
        )

    else:
        await dialog_manager.start(
            BoilerRegistrationDialog.boiler_registration_user_name
        )


async def confirm_sending_tech_catalog_request(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_id = str(callback.from_user.id)
    user_data = User.get_user_by_telegram_id(user_id)

    if user_data:
        radio_catalog_widget = dialog_manager.find(
            'tech_catalog'
        )
        radio_catalog_widget: ManagedRadio

        user_technical_type = TECHNICAL_CATALOG.get(radio_catalog_widget.get_checked(), 'ERROR')

        request_title = dialog_manager.dialog_data['button_click']
        user_phone = dialog_manager.dialog_data['user_phone']
        user_name = dialog_manager.dialog_data['user_name']
        firm_type = dialog_manager.dialog_data['firm_type']

        user_address = dialog_manager.dialog_data.get('user_address', '—')
        user_budget = dialog_manager.dialog_data.get('user_budget', '—')
        place_format = dialog_manager.dialog_data.get('place_format', '—')

        task_description = (f"\n"
                            f"Бюджет: {user_budget}\n\n"
                            f"Формат заведения: {place_format}\n\n"
                            f"Тип кофемашины: {user_technical_type}\n\n")

        if firm_type == 'legal_entity':
            organization_itn = user_data['organization_itn']
            organization_name = user_data['organization_name']
            await send_form_task(
                callback=callback,
                user_name=user_name,
                user_phone=user_phone,
                user_address=user_address,
                task_title=request_title,
                task_description=task_description,
                dialog_manager=dialog_manager,
                organization_name=organization_name,
                organization_itn=organization_itn,
                firm_type=firm_type
            )
        else:
            await send_form_task(
                callback=callback,
                user_name=user_name,
                user_phone=user_phone,
                user_address=user_address,
                task_title=request_title,
                task_description=task_description,
                dialog_manager=dialog_manager,
                firm_type=firm_type
            )

    else:
        await dialog_manager.start(BoilerRegistrationDialog.boiler_registration_user_name)


async def confirm_rent_request_sending(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_id = str(callback.from_user.id)

    user_data = User.get_user_by_telegram_id(
        user_id
    )

    if user_data:

        rent_radio_rent_type_widget = dialog_manager.find(
            'rent_type'
        )
        rent_radio_catalog_widget = dialog_manager.find(
            'rent_tech_type'
        )

        rent_radio_rent_type_widget: ManagedRadio
        rent_radio_catalog_widget: ManagedRadio

        user_rent_type = RENT_TYPE.get(rent_radio_rent_type_widget.get_checked(), 'ERROR')
        user_technical_type = TECHNICAL_CATALOG.get(rent_radio_catalog_widget.get_checked(), 'ERROR')

        request_title = dialog_manager.dialog_data['button_click']
        user_phone = dialog_manager.dialog_data['user_phone']
        user_name = dialog_manager.dialog_data['user_name']
        firm_type = dialog_manager.dialog_data['firm_type']

        user_address = 'Отсутствует'

        task_description = (f"\n"
                            f"Тип аренды: {user_rent_type}\n\n"
                            f"Тип кофемашины: {user_technical_type}\n\n")

        if firm_type == 'legal_entity':
            organization_itn = user_data['organization_itn']
            organization_name = user_data['organization_name']
            await send_form_task(
                callback=callback,
                user_name=user_name,
                user_phone=user_phone,
                user_address=user_address,
                task_title=request_title,
                task_description=task_description,
                dialog_manager=dialog_manager,
                organization_name=organization_name,
                organization_itn=organization_itn,
                firm_type=firm_type
            )
        else:
            await send_form_task(
                callback=callback,
                user_name=user_name,
                user_phone=user_phone,
                user_address=user_address,
                task_title=request_title,
                task_description=task_description,
                dialog_manager=dialog_manager,
                firm_type=firm_type
            )

    else:
        await dialog_manager.start(
            BoilerRegistrationDialog.boiler_registration_user_name
        )


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
        user_phone = dialog_manager.dialog_data['user_phone']
        user_name = dialog_manager.dialog_data['user_name']
        firm_type = dialog_manager.dialog_data['firm_type']

        user_address = 'Отсутствует'

        task_description = (f"\n"
                            f"Количество человек на обучение: {barista_value}\n\n")

        if firm_type == 'legal_entity':
            organization_itn = user_data['organization_itn']
            organization_name = user_data['organization_name']
            await send_form_task(
                callback=callback,
                user_name=user_name,
                user_phone=user_phone,
                user_address=user_address,
                task_title=request_title,
                task_description=task_description,
                dialog_manager=dialog_manager,
                organization_name=organization_name,
                organization_itn=organization_itn,
                firm_type=firm_type
            )
        else:
            await send_form_task(
                callback=callback,
                user_name=user_name,
                user_phone=user_phone,
                user_address=user_address,
                task_title=request_title,
                task_description=task_description,
                dialog_manager=dialog_manager,
                firm_type=firm_type
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
