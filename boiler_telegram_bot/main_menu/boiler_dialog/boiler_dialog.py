from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row
from aiogram_dialog.widgets.text import Format

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_message_input_handlers import feedback_handler
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_on_click_functions import send_feedback
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog

boiler_main_menu = Window(
    Format(
        text='Добро пожаловать в официального бота компании BOILER.'
    ),
    Row(
        SwitchTo(
            id='repair', text=Format('Ремонт'), state=BoilerDialog.boiler_repair_menu
        ),
        SwitchTo(
            id='text_back', text=Format('Обратная связь'), state=BoilerDialog.boiler_feedback
        )
    ),
    state=BoilerDialog.boiler_main_menu
)

boiler_feedback = Window(
    Format(
        text='Отправьте в чат с ботом сообщение с обратной связью и мы обязательно его передадим нашим специалистам:'
    ),
    MessageInput(
        feedback_handler
    ),
    SwitchTo(
        id='back_to_menu', text=Format('В меню'), state=BoilerDialog.boiler_main_menu
    ),
    state=BoilerDialog.boiler_feedback
)

boiler_accept_feedback = Window(
    Format(
        text='<b>- {dialog_data[user_answer]}</b>'
    ),
    Button(
        id='send_feedback', text=Format('Отправить фидбек'), on_click=send_feedback
    ),
    Row(
        SwitchTo(
            id='back_to_feedback', text=Format('Назад'), state=BoilerDialog.boiler_feedback
        ),
        SwitchTo(
            id='back_to_menu', text=Format('В меню'), state=BoilerDialog.boiler_main_menu
        ),
    ),
    state=BoilerDialog.boiler_accept_feedback,
    parse_mode=ParseMode.HTML,
)

boiler_repair_menu = Window(
    Format(
        text='Hello'
    ),
    SwitchTo(
        id='back_to_menu', text=Format('В меню'), state=BoilerDialog.boiler_main_menu
    ),
    state=BoilerDialog.boiler_repair_menu
)

boiler_dialog = Dialog(
    boiler_main_menu,

    boiler_feedback,
    boiler_accept_feedback,

    boiler_repair_menu
)
