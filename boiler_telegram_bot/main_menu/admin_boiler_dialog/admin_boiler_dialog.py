from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format

from main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import feedback_count_getter
from main_menu.admin_boiler_dialog.admin_boiler_dialog_on_click_functions import go_to_boiler_bot
from main_menu.admin_boiler_dialog.boiler_dialog_states import AdminBoilerDialog

from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_dataclasses import FEEDBACK_KEY
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import new_feedbacks_getter, \
    feedback_id_getter

admin_boiler_main_menu = Window(
    Format(
        text='Добро пожаловать в административную панель бота Boiler.\n\n'
             'Непросмотренных отзывов: {feedbacks_count}'
    ),
    Button(
        id='go_to_boiler', text=Format('Перейти в бота'), on_click=go_to_boiler_bot
    ),
    Row(
        SwitchTo(
            id='view_feedbacks', text=Format('Просмотр фидбеков'),
            state=AdminBoilerDialog.admin_boiler_feedbacks_menu
        ),
        SwitchTo(
            id='view_problems', text=Format('Редактирование проблем'),
            state=AdminBoilerDialog.admin_boiler_technical_problems
        ),
    ),
    getter=feedback_count_getter,
    state=AdminBoilerDialog.admin_boiler_main_menu
)

admin_boiler_feedbacks = Window(
    Format(
        text='Непросмотренных отзывов: {feedbacks_count}'
    ),
    Row(
        SwitchTo(
            id='new_feedbacks', text=Format('Новые отзывы'), state=AdminBoilerDialog.admin_boiler_new_feedbacks,
            when=F['feedbacks_count'] > 0
        ),
        SwitchTo(
            id='old_feedbacks', text=Format('Просмотренные отзывы'), state=AdminBoilerDialog.admin_boiler_old_feedbacks,
            when=F['feedbacks_count'] == 0
        )
    ),
    getter=feedback_count_getter,
    state=AdminBoilerDialog.admin_boiler_feedbacks_menu
)

admin_boiler_new_feedbacks = Window(
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.title}"),
                id="shop_item_select",
                items=FEEDBACK_KEY,
                item_id_getter=feedback_id_getter,
                on_click=on_shop_item_selected,
            ),
        ),
        width=1,
        height=5,
        id="scroll_executors_menu",
        when=F["dialog_data"],
        hide_on_single_page=True,
    ),
    state=AdminBoilerDialog.admin_boiler_new_feedbacks,
    getter=new_feedbacks_getter
)

admin_boiler_dialog = Dialog(
    admin_boiler_main_menu
)
