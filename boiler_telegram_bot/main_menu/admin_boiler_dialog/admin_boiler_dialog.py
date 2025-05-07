from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format

from main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import feedback_count_getter
from main_menu.admin_boiler_dialog.admin_boiler_dialog_on_click_functions import go_to_boiler_bot
from main_menu.admin_boiler_dialog.boiler_dialog_states import AdminBoilerDialog

admin_boiler_main_menu = Window(
    Format(
        text='Добро пожаловать в административную панель бота Boiler.\n\n'
             'Непросмотренных фидбеков: {feedbacks_count}'
    ),
    Button(
        id='go_to_boiler', text=Format('Перейти в бота'), on_click=go_to_boiler_bot
    ),
    Row(
        SwitchTo(
            id='view_feedbacks', text=Format('Просмотр фидбеков'),
            state=AdminBoilerDialog.admin_boiler_feedbacks
        ),
        SwitchTo(
            id='view_problems', text=Format('Редактирование проблем'),
            state=AdminBoilerDialog.admin_boiler_technical_problems
        ),
    ),
    getter=feedback_count_getter,
    state=AdminBoilerDialog.admin_boiler_main_menu
)

# admin_boiler_feedbacks = Window(
#     ScrollingGroup(
#         Column(
#             Select(
#                 text=Format("{item.name}"),
#                 id="tech_prob_group",
#                 items=TECHNICAL_PROBLEM_KEY,
#                 item_id_getter=technical_problem_id_getter,
#                 on_click=on_technical_problem_selected,
#             ),
#         ),
#         width=1,
#         height=5,
#         id="scroll_tech_prob_menu",
#         hide_on_single_page=True,
#     ),
#     getter=None,
#     state=AdminBoilerDialog.admin_boiler_feedbacks
# )

admin_boiler_dialog = Dialog(
    admin_boiler_main_menu
)
