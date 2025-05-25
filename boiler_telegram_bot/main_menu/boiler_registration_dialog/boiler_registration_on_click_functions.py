from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button

from boiler_telegram_bot.db_configuration.models.user import User
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog


async def user_registration(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    user_phone = dialog_manager.dialog_data['user_phone']
    user_name = dialog_manager.dialog_data['user_name']
    organization_itn = dialog_manager.dialog_data['organization_itn']
    organization_name = dialog_manager.dialog_data['organization_name']

    telegram_id = str(callback.from_user.id)
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

    User.add_user(
        telegram_id=telegram_id,
        telegram_first_name=user_first_name,
        telegram_last_name=user_last_name,
        telegram_username=user_username,
        name=user_name,
        organization_name=organization_name,
        organization_itn=organization_itn,
        phone=user_phone
    )

    await callback.message.answer(
        text='🎉 Вы успешно зарегистрировались! 🚀'
    )

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    await dialog_manager.start(
        BoilerDialog.boiler_main_menu,
    )