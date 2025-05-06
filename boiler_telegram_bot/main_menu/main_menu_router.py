from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram_dialog import DialogManager

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog

main_menu_router = Router()


@main_menu_router.message(Command('start'))
async def start_dialog_command(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        BoilerDialog.boiler_main_menu,
        data={'user_id': message.from_user.id}
    )


@main_menu_router.message(F.text)
async def start_dialog_text(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        BoilerDialog.boiler_main_menu,
        data={'user_id': message.from_user.id},
    )
