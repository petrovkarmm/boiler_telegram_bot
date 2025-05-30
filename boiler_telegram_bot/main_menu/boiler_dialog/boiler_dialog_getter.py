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
