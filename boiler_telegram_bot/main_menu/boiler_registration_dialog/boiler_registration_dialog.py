from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Button
from aiogram_dialog.widgets.text import Format

from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_message_input_handlers import name_handler, phone_handler, \
    organization_itn_handler, organization_name_handler
from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_on_click_functions import user_registration
from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog

boiler_registration_user_name = Window(
    Format(
        text=(
            "📝 <b>Регистрация</b>\n\n"
            "Чтобы продолжить использовать бота, необходимо пройти короткую регистрацию.\n\n"
            "🙋‍♂️ Пожалуйста, напишите, как к вам можно обращаться (ваше имя):"
        )
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
            "📞 <b>Номер телефона</b>\n\n"
            "Пожалуйста, укажите номер для связи с вами.\n"
            "Допустимый формат: <b>+7XXXXXXXXXX</b> или <b>8XXXXXXXXXX</b>\n\n"
            "Убедитесь, что номер введён корректно — мы свяжемся с вами по нему."
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
        text=(
            "🏢 <b>Название юр. лица</b>\n\n"
            "Введите, пожалуйста, название вашего юр. лица:"
        )
    ),
    MessageInput(
        organization_name_handler
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerRegistrationDialog.boiler_registration_phone
        ),
        SwitchTo(
            id='start_again', text=Format('🔁 Начать сначала'),
            state=BoilerRegistrationDialog.boiler_registration_user_name
        )
    ),
    state=BoilerRegistrationDialog.boiler_registration_organization_name,
    parse_mode=ParseMode.HTML
)

boiler_registration_organization_itn = Window(
    Format(
        text=(
            "🧾 <b>ИНН юр. лица</b>\n\n"
            "Пожалуйста, введите ИНН вашего юр. лица:"
        )
    ),
    MessageInput(
        organization_itn_handler
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'),
            state=BoilerRegistrationDialog.boiler_registration_organization_name
        ),
        SwitchTo(
            id='start_again', text=Format('🔁 Начать сначала'),
            state=BoilerRegistrationDialog.boiler_registration_user_name
        )
    ),
    state=BoilerRegistrationDialog.boiler_registration_itn,
    parse_mode=ParseMode.HTML
)

boiler_registration_accepting = Window(
    Format(
        text=(
            "✅ <b>Проверьте введённые данные:</b>\n\n"
            "📞 <b>Телефон:</b> {dialog_data[user_phone]}\n"
            "👤 <b>Имя:</b> {dialog_data[user_name]}\n"
            "🏢 <b>Юр. лицо:</b> {dialog_data[organization_name]}\n"
            "🧾 <b>ИНН:</b> {dialog_data[organization_itn]}"
        )
    ),
    Button(
        id='registration', text=Format('🚀 Зарегистрироваться'), on_click=user_registration
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerRegistrationDialog.boiler_registration_itn
        ),
        SwitchTo(
            id='start_again', text=Format('🔁 Начать сначала'),
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
