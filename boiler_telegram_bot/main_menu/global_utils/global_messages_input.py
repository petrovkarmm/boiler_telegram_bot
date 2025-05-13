from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog


async def get_itn_and_organization_name(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager
):
    user_answer = message.text

    dialog_manager.dialog_data['user_itn_and_organization_name'] = user_answer

    await dialog_manager.switch_to(
        BoilerDialog.boiler_barista_training_accept_request
    )