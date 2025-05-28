from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedRadio

from boiler_telegram_bot.db_configuration.models.technical_problem import TechnicalProblem
from boiler_telegram_bot.db_configuration.models.user import User
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_dataclasses import TechnicalProblemDialog, \
    TECHNICAL_PROBLEM_KEY, \
    TECHNICAL_CATALOG, RENT_TYPE, ProfileDialog, PROFILE_KEY
from boiler_telegram_bot.tg_logs.logger import bot_logger
from boiler_telegram_bot.db_configuration.models.firm import Firm


def technical_problem_id_getter(technical_problem: TechnicalProblemDialog) -> int:
    return technical_problem.id


def profile_id_getter(profile: ProfileDialog) -> int:
    return profile.id


async def profiles_getter(dialog_manager: DialogManager, **_kwargs):
    event_update = _kwargs.get('event_update')

    user_id = str(event_update.event.from_user.id)

    user_firms = Firm.get_firms_by_telegram_id(user_id)

    return {
        PROFILE_KEY: [
            ProfileDialog(
                firm['firm_id'], ProfileDialog.formatted_name(name=firm['name'], firm_type=firm['firm_type'])
            )
            for firm in user_firms
        ]
    }


async def technical_catalog_getter(**kwargs):
    catalog = [
        ("Рожковая", "horn"),
        ("Автоматическая", "auto"),
    ]
    return {"catalog": catalog}


async def rent_type_getter(**kwargs):
    rents = [
        ("Суточная", "daily"),
        ("Помесячная", "monthly"),
    ]
    return {"rents": rents}


async def video_or_photo_format_data(dialog_manager: DialogManager, **_kwargs):
    dialog_manager.dialog_data['filename'] = None
    dialog_manager.dialog_data['tmp_file_path'] = None

    return {

    }


async def get_technical_catalog_data_for_accept(dialog_manager: DialogManager, **_kwargs):
    event_update = _kwargs.get('event_update')

    user_id = str(event_update.event.from_user.id)

    user_data = User.get_user_by_telegram_id(
        user_id
    )

    if user_data:
        radio_widget = dialog_manager.find(
            'tech_catalog'
        )
        radio_widget: ManagedRadio

        user_technical_type = TECHNICAL_CATALOG.get(radio_widget.get_checked(), 'ERROR')
        user_address = dialog_manager.dialog_data['user_address']
        user_budget = dialog_manager.dialog_data['user_budget']
        place_format = dialog_manager.dialog_data['place_format']
        user_phone = user_data['phone']
        user_name = user_data['name']
        organization_itn = user_data['organization_itn']
        organization_name = user_data['organization_name']

        return {
            "user_address": user_address,
            "user_budget": user_budget,
            "place_format": place_format,
            "user_phone": user_phone,
            "user_name": user_name,
            "organization_itn": organization_itn,
            "organization_name": organization_name,
            "user_technical_type": user_technical_type
        }


    else:
        bot_logger.warning(
            f'Незарегистрированный пользователь в меню. | {user_id}'
        )
        return None


async def user_data_profile_getter(dialog_manager: DialogManager, **_kwargs):
    event_update = _kwargs.get('event_update')

    user_id = str(event_update.event.from_user.id)

    user_data = User.get_user_by_telegram_id(
        user_id
    )

    if user_data:
        user_phone = user_data['phone']
        user_name = user_data['name']
        organization_itn = user_data['organization_itn']
        organization_name = user_data['organization_name']

        return {
            'user_phone': user_phone,
            'user_name': user_name,
            'organization_name': organization_name,
            'organization_itn': organization_itn,
        }
    else:
        bot_logger.warning(
            f'Незарегистрированный пользователь в меню. | {user_id}'
        )
        return None


async def technical_problems_getter(**_kwargs):
    technical_problems = TechnicalProblem.get_all_unhidden_technical_problem()

    return {
        TECHNICAL_PROBLEM_KEY: [
            TechnicalProblemDialog(
                technical_problem["id"], technical_problem["name"]
            )
            for technical_problem in technical_problems
        ]
    }
