from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from boiler_telegram_bot.db_configuration.models.user import User
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog
from boiler_telegram_bot.db_configuration.models.firm import Firm
from boiler_telegram_bot.db_configuration.models.firm_info_individual import FirmInfoIndividual
from boiler_telegram_bot.db_configuration.models.firm_info_legal_entity import FirmInfoLegalEntity


async def choose_legal_entity(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['firm_type'] = 'legal_entity'
    await dialog_manager.switch_to(
        BoilerRegistrationDialog.boiler_registration_organization_name
    )


async def choose_individual(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['firm_type'] = 'individual'
    await dialog_manager.switch_to(
        BoilerRegistrationDialog.boiler_registration_accepting
    )


async def user_registration(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    firm_type = dialog_manager.dialog_data['firm_type']
    user_phone = dialog_manager.dialog_data['user_phone']
    user_name = dialog_manager.dialog_data['user_name']

    if firm_type == 'legal_entity':
        organization_itn = dialog_manager.dialog_data['organization_itn']
        organization_name = dialog_manager.dialog_data['organization_name']
    elif firm_type == 'individual':
        organization_itn = organization_name = None
    else:
        await callback.message.answer(
            text='⚠️ Упс! Кажется, что-то пошло не так.',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
        await dialog_manager.start(BoilerRegistrationDialog.boiler_registration_user_name)
        return

    telegram_id = str(callback.from_user.id)
    user_username = f"@{callback.from_user.username}" if callback.from_user.username else 'Username отсутствует'
    user_first_name = callback.from_user.first_name or 'Имя отсутствует'
    user_last_name = callback.from_user.last_name or 'Фамилия отсутствует'

    user_id = User.add_user(
        telegram_id=telegram_id,
        telegram_first_name=user_first_name,
        telegram_last_name=user_last_name,
        telegram_username=user_username,
    )

    firm_id = Firm.add_firm(user_id=user_id, firm_type=firm_type)

    if firm_type == 'legal_entity':
        FirmInfoLegalEntity.add_info(
            firm_id=firm_id,
            organization_name=organization_name,
            representative_name=user_name,
            organization_itn=organization_itn,
            phone=user_phone
        )
    elif firm_type == 'individual':
        FirmInfoIndividual.add_info(
            firm_id=firm_id,
            name=user_name,
            phone=user_phone
        )

    await callback.message.answer(text='🎉 Вы успешно зарегистрировались! 🚀')
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await dialog_manager.start(BoilerDialog.boiler_main_menu)
