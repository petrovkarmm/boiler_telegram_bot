from pprint import pprint

from aiogram.types import Update
from aiogram_dialog import DialogManager

from db_configuration.models.technical_problem import TechnicalProblem
from db_configuration.models.user import User
from main_menu.boiler_dialog.boiler_dialog_dataclasses import TechnicalProblemDialog, TECHNICAL_PROBLEM_KEY
from main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog


def technical_problem_id_getter(technical_problem: TechnicalProblemDialog) -> int:
    return technical_problem.id


async def user_data_getter(dialog_manager: DialogManager, **_kwargs):
    event_update = _kwargs.get('event_update')

    user_id = event_update.event.from_user.id

    user_data = User.get_user_by_telegram_id(
        user_id
    )

    if user_data:
        user_phone = user_data['user_phone']
        user_name = user_data['user_name']
        return {
            'user_phone': user_phone,
            'user_name': user_name
        }
    else:
        await dialog_manager.start(
            BoilerRegistrationDialog.boiler_registration_user_name
        )


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
