from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from main_menu.boiler_dialog.utils import normalize_phone_number
from main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog


async def name_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data['user_name'] = message.text
    await dialog_manager.switch_to(
        BoilerRegistrationDialog.boiler_registration_phone
    )


async def organization_itn_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data['organization_itn'] = message.text
    await dialog_manager.switch_to(
        BoilerRegistrationDialog.boiler_registration_accepting
    )


async def organization_name_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data['organization_name'] = message.text
    await dialog_manager.switch_to(
        BoilerRegistrationDialog.boiler_registration_itn
    )


async def phone_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_phone = message.text

    validate_user_phone = await normalize_phone_number(
        user_phone
    )

    if validate_user_phone:
        dialog_manager.dialog_data['user_phone'] = validate_user_phone
        await dialog_manager.switch_to(
            BoilerRegistrationDialog.boiler_registration_organization_name
        )

    else:
        await message.answer(
            text="❌ <b>Некорректный номер телефона</b>\n\n"
                 "Пожалуйста, введите номер в одном из следующих форматов:\n"
                 "📱 <code>+7XXXXXXXXXX</code> или <code>8XXXXXXXXXX</code>\n\n"
                 "Попробуйте ещё раз 👇",
            parse_mode=ParseMode.HTML
        )
