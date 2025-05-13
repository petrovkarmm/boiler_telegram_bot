from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Button
from aiogram_dialog.widgets.text import Format

from main_menu.boiler_registration_dialog.boiler_registration_message_input_handlers import name_handler, phone_handler, \
    organization_itn_handler, organization_name_handler
from main_menu.boiler_registration_dialog.boiler_registration_on_click_functions import user_registration
from main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog

boiler_registration_user_name = Window(
    Format(
        text='Для дальнейшего использования бота необходимо провести регистрацию. \n\n'
             '🙋 Как к вам можно обращаться? Напишите ваше имя.'
    ),
    MessageInput(
        name_handler
    ),
    state=BoilerRegistrationDialog.boiler_registration_user_name,
    parse_mode=ParseMode.HTML
)

boiler_registration_phone = Window(
    Format(
        text=(
            '📞 Пожалуйста, укажите номер телефона для связи.\n'
            'Формат: <b>+7XXXXXXXXXX</b> или <b>8XXXXXXXXXX</b>'
        )
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerRegistrationDialog.boiler_registration_user_name
        ),
    ),
    MessageInput(
        phone_handler
    ),
    state=BoilerRegistrationDialog.boiler_registration_phone,
    parse_mode=ParseMode.HTML,
)

boiler_registration_organization_name = Window(
    Format(
        text='Введите Название организации:'
    ),
    MessageInput(
        organization_name_handler
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerRegistrationDialog.boiler_registration_itn
        ),
        SwitchTo(
            id='start_again', text=Format('Начать сначала'),
            state=BoilerRegistrationDialog.boiler_registration_user_name
        )
    ),
    state=BoilerRegistrationDialog.boiler_registration_organization_name,
    parse_mode=ParseMode.HTML
)

boiler_registration_organization_itn = Window(
    Format(
        text='Введите ИНН организации:'
    ),
    MessageInput(
        organization_itn_handler
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerRegistrationDialog.boiler_registration_phone
        ),
        SwitchTo(
            id='start_again', text=Format('Начать сначала'),
            state=BoilerRegistrationDialog.boiler_registration_user_name
        )
    ),
    state=BoilerRegistrationDialog.boiler_registration_itn,
    parse_mode=ParseMode.HTML
)

boiler_registration_accepting = Window(
    Format(
        text='Проверьте данные перед регистрацией:\n\n'
             '{dialog_data[user_phone]}'
             '{dialog_data[user_name]}'
             '{dialog_data[organization_itn]}'
             '{dialog_data[organization_name]}'
    ),
    Button(
        id='registration', text=Format('Зарегистрироваться'), on_click=user_registration
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerRegistrationDialog.boiler_registration_phone
        ),
        SwitchTo(
            id='start_again', text=Format('Начать сначала'),
            state=BoilerRegistrationDialog.boiler_registration_user_name
        )
    ),
    state=BoilerRegistrationDialog.boiler_registration_accepting,
    parse_mode=ParseMode.HTML
)

boiler_registration_dialog = Dialog(
    boiler_registration_user_name,
    boiler_registration_phone,
    boiler_registration_organization_itn,
    boiler_registration_organization_name,
    boiler_registration_accepting
)
