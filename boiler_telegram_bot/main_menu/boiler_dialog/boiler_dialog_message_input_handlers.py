from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Format
from aiogram.types import Message

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog


async def feedback_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_answer = message.text
    if user_answer:
        dialog_manager.dialog_data['user_answer'] = user_answer
        await dialog_manager.switch_to(
            BoilerDialog.boiler_accept_feedback
        )
    else:
        await message.answer(
            text='Кажется, вы отправили что-то другое... =/'
        )
