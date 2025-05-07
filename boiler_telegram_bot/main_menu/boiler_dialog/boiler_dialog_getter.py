from aiogram_dialog import DialogManager

from db_configuration.crud import TechnicalProblem
from main_menu.boiler_dialog.boiler_dialog_dataclasses import TechnicalProblemDialog, TECHNICAL_PROBLEM_KEY


def technical_problem_id_getter(technical_problem: TechnicalProblemDialog) -> int:
    return TechnicalProblemDialog.id


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
