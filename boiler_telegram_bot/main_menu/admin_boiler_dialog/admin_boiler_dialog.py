from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format

from main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import feedbacks_count_getter, feedback_getter, \
    technical_problem_id_getter, technical_problems_getter, technical_problem_getter
from main_menu.admin_boiler_dialog.admin_boiler_dialog_on_click_functions import go_to_boiler_bot, \
    on_feedback_selected, go_to_new_feedbacks, go_to_old_feedbacks, mark_feedback, on_technical_problem_selected
from main_menu.admin_boiler_dialog.admin_boiler_dialog_states import AdminBoilerDialog

from main_menu.admin_boiler_dialog.admin_boiler_dialog_dataclasses import ADMIN_FEEDBACK_KEY, \
    ADMIN_TECHNICAL_PROBLEM_KEY
from main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import feedbacks_getter, \
    feedback_id_getter

admin_boiler_main_menu = Window(
    Format(
        text='Добро пожаловать в административную панель бота Boiler.\n\n'
             'Непросмотренных отзывов: {new_feedbacks_count}'
    ),
    Row(
        SwitchTo(
            id='view_feedbacks', text=Format('Просмотр фидбеков'),
            state=AdminBoilerDialog.admin_boiler_feedbacks_menu
        ),
        SwitchTo(
            id='view_problems', text=Format('Редактирование проблем'),
            state=AdminBoilerDialog.admin_boiler_technical_problems_list
        ),
    ),
    Button(
        id='go_to_boiler', text=Format('Перейти в бота'), on_click=go_to_boiler_bot
    ),
    getter=feedbacks_count_getter,
    state=AdminBoilerDialog.admin_boiler_main_menu
)

admin_boiler_feedbacks = Window(
    Format(
        text='Непросмотренных отзывов: {new_feedbacks_count}',
    ),
    Row(
        Button(
            id='new_feedbacks', text=Format('Новые отзывы'), on_click=go_to_new_feedbacks,
            when=F['new_feedbacks_count'] > 0
        ),
        Button(
            id='old_feedbacks', text=Format('Просмотренные отзывы'), on_click=go_to_old_feedbacks,
            when=F['old_feedbacks_count'] > 0
        )
    ),
    Row(
        SwitchTo(
            id='back_to_menu', text=Format('В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=feedbacks_count_getter,
    state=AdminBoilerDialog.admin_boiler_feedbacks_menu
)

admin_boiler_feedbacks_list = Window(
    Format(
        text='Непросмотренные отзывы отсутствуют.',
        when=F['new_feedbacks_count'] == 0 and F['dialog_data']['feedback_menu'] == 'new'
    ),
    Format(
        text='Выберите фидбек для прочтения:',
        when=F['new_feedbacks_count'] > 0
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.feedback_text}"),
                id="feedback_selected",
                items=ADMIN_FEEDBACK_KEY,
                item_id_getter=feedback_id_getter,
                on_click=on_feedback_selected,
            ),
        ),
        width=1,
        height=5,
        id="scroll_new_fb",
        hide_on_single_page=True,
        when=F['new_feedbacks_count'] > 0
    ),
    Row(
        SwitchTo(
            id='back_to_fb_menu', text=Format('Назад'), state=AdminBoilerDialog.admin_boiler_feedbacks_menu
        ),
        SwitchTo(
            id='back_to_menu', text=Format('В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=feedbacks_getter,
    state=AdminBoilerDialog.admin_boiler_feedbacks_list,
)

admin_boiler_feedback_view = Window(
    Format(
        text='Дата отправки фидбека: <b>{created}</b>\n\n'
             'Текст фидбека: <b>{feedback_text}</b>\n\n'
             'Данные об отправителе: \n\n'
             'Телеграм ID: {tg_user_id}\n'
             '{user_username} | {user_lastname} | {user_firstname}'
    ),
    Button(
        id='mark_feedback', text=Format('Отметить прочтённым'), on_click=mark_feedback,
        when=F['dialog_data']['feedback_menu'] == 'new'
    ),
    Row(
        SwitchTo(
            id='back_to_new_fb_menu', text=Format('Назад'), state=AdminBoilerDialog.admin_boiler_feedbacks_list
        ),
        SwitchTo(
            id='back_to_menu', text=Format('В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=feedback_getter,
    state=AdminBoilerDialog.admin_boiler_feedback_view,
    parse_mode=ParseMode.HTML
)

technical_problem_view = Window(
    Format(
        text='Test'
    ),
    Row(
        SwitchTo(
            id='back_to_new_fb_menu', text=Format('Назад'), state=AdminBoilerDialog.admin_boiler_technical_problems_list
        ),
        SwitchTo(
            id='back_to_menu', text=Format('В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=technical_problem_getter,
    state=AdminBoilerDialog.admin_boiler_technical_problem_view
)

admin_boiler_technical_problems_list = Window(
    Format(
        text='Выберите проблему для редактирования:'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.name}"),
                id="problem_selected",
                items=ADMIN_TECHNICAL_PROBLEM_KEY,
                item_id_getter=technical_problem_id_getter,
                on_click=on_technical_problem_selected,
            ),
        ),
        width=1,
        height=5,
        id="scroll_tech_pb",
        hide_on_single_page=True,
    ),
    SwitchTo(
        id='back_to_menu', text=Format('В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
    ),
    getter=technical_problems_getter,
    state=AdminBoilerDialog.admin_boiler_technical_problems_list
)

admin_boiler_dialog = Dialog(
    admin_boiler_main_menu,

    admin_boiler_feedbacks,
    admin_boiler_feedbacks_list,
    admin_boiler_feedback_view,

    admin_boiler_technical_problems_list,
    technical_problem_view
)
