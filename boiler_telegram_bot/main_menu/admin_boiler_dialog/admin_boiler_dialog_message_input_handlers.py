from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from db_configuration.models.technical_problem import TechnicalProblem
from main_menu.admin_boiler_dialog.admin_boiler_dialog_states import AdminBoilerDialog


async def new_technical_problem_name_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    new_technical_problem_name = message.text

    TechnicalProblem.add_technical_problem(
        name=new_technical_problem_name, hidden=1
    )

    await dialog_manager.switch_to(
        AdminBoilerDialog.admin_boiler_technical_problems_list
    )
