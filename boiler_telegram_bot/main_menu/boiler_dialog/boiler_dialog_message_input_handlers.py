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
        if len(user_answer) >= 1000:
            await message.answer(
                text='Ответ должен быть менее 1000 символов!'
            )
        else:
            dialog_manager.dialog_data['user_answer'] = user_answer
            await dialog_manager.switch_to(
                BoilerDialog.boiler_accept_feedback
            )
    else:
        await message.answer(
            text='Кажется, вы отправили что-то другое... =/'
        )


async def technical_problem_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_technical_problem = message.text
    if user_technical_problem:
        if len(user_technical_problem) >= 1000:
            await message.answer(
                text='Тема проблемы должна быть менее 1000 символов!'
            )
        else:
            dialog_manager.dialog_data['technical_problem'] = user_technical_problem
            await dialog_manager.switch_to(
                BoilerDialog.boiler_repair_description
            )
    else:
        await message.answer(
            text='Кажется, вы отправили что-то другое... =/'
        )
