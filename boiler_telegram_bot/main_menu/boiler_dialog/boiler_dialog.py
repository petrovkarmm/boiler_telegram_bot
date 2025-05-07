from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_message_input_handlers import feedback_handler, \
    technical_problem_handler
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_on_click_functions import send_feedback, \
    on_technical_problem_selected
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from main_menu.boiler_dialog.boiler_dialog_dataclasses import TECHNICAL_PROBLEM_KEY
from main_menu.boiler_dialog.boiler_dialog_getter import technical_problem_id_getter, technical_problems_getter

boiler_main_menu = Window(
    Format(
        text='Здравствуйте!\n\n'
             'В какой раздел сервиса вы хотите обратиться?'
    ),
    Row(
        SwitchTo(
            id='repair', text=Format('Ремонт'), state=BoilerDialog.boiler_repair_problem
        ),
        SwitchTo(
            id='tech_cat', text=Format('Подбор техники'), state=BoilerDialog.boiler_technical_catalog
        ),
    ),
    Row(
        SwitchTo(
            id='rent', text=Format('Аренда'), state=BoilerDialog.boiler_rent
        ),
        SwitchTo(
            id='bar_training', text=Format('Обучение Бариста'), state=BoilerDialog.boiler_barista_training
        ),
    ),
    SwitchTo(
        id='text_back', text=Format('Обратная связь'), state=BoilerDialog.boiler_feedback
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

boiler_repair_problem = Window(
    Format("Выберите тему заявки из списка, если нужной темы в списке нет - отправьте тему сообщением в чат:"),
    ScrollingGroup(
        Column(
            Select(
                text=Format("<b>{item.name}</b>"),
                id="tech_prob_group",
                items=TECHNICAL_PROBLEM_KEY,
                item_id_getter=technical_problem_id_getter,
                on_click=on_technical_problem_selected,
            ),
        ),
        width=1,
        height=5,
        id="scroll_tech_prob_menu",
        hide_on_single_page=True,
    ),
    SwitchTo(
        id='back_to_menu', text=Format('В меню'), state=BoilerDialog.boiler_main_menu
    ),
    MessageInput(
        technical_problem_handler
    ),
    getter=technical_problems_getter,
    state=BoilerDialog.boiler_repair_problem,
    parse_mode=ParseMode.HTML,
)

boiler_repair_description = Window(
    Format(
        text='<b>Тема проблемы: {dialog_data[technical_problem]}</b>'
    ),
    SwitchTo(
        id='back_to_t_pr', text=Format('Назад'), state=BoilerDialog.boiler_repair_problem
    ),
    SwitchTo(
        id='back_to_menu', text=Format('В меню'), state=BoilerDialog.boiler_main_menu
    ),
    state=BoilerDialog.boiler_repair_description,
    parse_mode=ParseMode.HTML,
)

boiler_dialog = Dialog(
    boiler_main_menu,

    boiler_feedback,
    boiler_accept_feedback,

    boiler_repair_problem,
    boiler_repair_description
)
