from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format

from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import feedbacks_count_getter, feedback_getter, \
    technical_problem_id_getter, technical_problems_getter, technical_problem_getter
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_message_input_handlers import new_technical_problem_name_handler
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_on_click_functions import go_to_boiler_bot, \
    on_feedback_selected, go_to_new_feedbacks, go_to_old_feedbacks, mark_feedback, on_technical_problem_selected, \
    toggle_technical_problem_hidden_status, deleting_technical_problem
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_states import AdminBoilerDialog

from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_dataclasses import ADMIN_FEEDBACK_KEY, \
    ADMIN_TECHNICAL_PROBLEM_KEY
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_getter import feedbacks_getter, \
    feedback_id_getter

admin_boiler_main_menu = Window(
    Format(
        text=(
            '👋 <b>Добро пожаловать в административную панель бота Boiler!</b>\n\n'
            '📬 <b>Непросмотренных отзывов:</b> <code>{new_feedbacks_count}</code>'
        )
    ),
    Row(
        SwitchTo(
            id='view_feedbacks', text=Format('📝 Отзывы'),
            state=AdminBoilerDialog.admin_boiler_feedbacks_menu
        ),
        SwitchTo(
            id='view_problems', text=Format('⚙️ Проблемы'),
            state=AdminBoilerDialog.admin_boiler_technical_problems_list
        ),
    ),
    Button(
        id='go_to_boiler', text=Format('🤖 Перейти в бота'), on_click=go_to_boiler_bot
    ),
    getter=feedbacks_count_getter,
    state=AdminBoilerDialog.admin_boiler_main_menu,
    parse_mode=ParseMode.HTML
)

admin_boiler_feedbacks = Window(
    Format(
        text=(
            '📝 <b>Управление отзывами</b>\n\n'
            '📬 <b>Новых отзывов:</b> <code>{new_feedbacks_count}</code>'
        )
    ),
    Row(
        Button(
            id='new_feedbacks', text=Format('🆕 Новые отзывы'), on_click=go_to_new_feedbacks,
            when=F['new_feedbacks_count'] > 0
        ),
        Button(
            id='old_feedbacks', text=Format('📂 Просмотренные отзывы'), on_click=go_to_old_feedbacks,
            when=F['old_feedbacks_count'] > 0
        )
    ),
    Row(
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=feedbacks_count_getter,
    state=AdminBoilerDialog.admin_boiler_feedbacks_menu,
    parse_mode=ParseMode.HTML
)

admin_boiler_feedbacks_list = Window(
    Format(
        text='✅ <b>Новых отзывов нет.</b>\n\nВсе отзывы были просмотрены 👀',
        when=(F['new_feedbacks_count'] == 0) & (F['dialog_data']['feedback_menu'] == 'new')
    ),
    Format(
        text='📝 <b>Выберите отзыв для прочтения:</b>',
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
        id="scroll_fb",
        hide_on_single_page=True,
    ),
    Row(
        SwitchTo(
            id='back_to_fb_menu', text=Format('⬅️ Назад'), state=AdminBoilerDialog.admin_boiler_feedbacks_menu
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=feedbacks_getter,
    state=AdminBoilerDialog.admin_boiler_feedbacks_list,
    parse_mode=ParseMode.HTML
)

admin_boiler_feedback_view = Window(
    Format(
        text=(
            '🗓️ <b>Дата отправки:</b> {created}\n\n'
            '💬 <b>Текст отзыва:</b>\n<blockquote>{feedback_text}</blockquote>\n\n'
            '🙋 <b>Информация об отправителе:</b>\n'
            '🆔 Telegram ID: <code>{tg_user_id}</code>\n'
            '👤 {user_username} | {user_lastname} | {user_firstname}'
        )
    ),
    Button(
        id='mark_feedback', text=Format('✅ Отметить прочитанным'), on_click=mark_feedback,
        when=F['dialog_data']['feedback_menu'] == 'new'
    ),
    Row(
        SwitchTo(
            id='back_to_new_fb_menu', text=Format('⬅️ Назад'), state=AdminBoilerDialog.admin_boiler_feedbacks_list
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=feedback_getter,
    state=AdminBoilerDialog.admin_boiler_feedback_view,
    parse_mode=ParseMode.HTML
)

admin_boiler_technical_problems_list = Window(
    Format(
        text='🛠️ <b>Выберите техническую проблему для редактирования:</b>'
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
        id='create_new_tp', text=Format('➕ Создать новую проблему'),
        state=AdminBoilerDialog.admin_boiler_technical_problem_create_new
    ),
    SwitchTo(
        id='back_to_menu', text=Format('🏠 В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
    ),
    getter=technical_problems_getter,
    state=AdminBoilerDialog.admin_boiler_technical_problems_list,
    parse_mode=ParseMode.HTML
)

admin_boiler_technical_problem_view = Window(
    Format(
        text=(
            '🛠️ <b>{technical_problem_name}</b>\n\n'
            '📌 <b>Статус:</b> {technical_problem_hidden}\n'
            '📅 <b>Создана:</b> {technical_problem_created}\n'
            '♻️ <b>Обновлена:</b> {technical_problem_updated}'
        )
    ),
    Button(
        id='edit_name', text=Format('🗑️ Удалить'), on_click=deleting_technical_problem
    ),
    Button(
        id='hide_problem', text=Format('🙈 Скрыть'), on_click=toggle_technical_problem_hidden_status,
        when=F['technical_problem_hidden'] == 'Отображается'
    ),
    Button(
        id='open_problem', text=Format('👁️ Отобразить'), on_click=toggle_technical_problem_hidden_status,
        when=F['technical_problem_hidden'] == 'Скрыт'
    ),
    Row(
        SwitchTo(
            id='back_to_new_fb_menu', text=Format('⬅️ Назад'), state=AdminBoilerDialog.admin_boiler_technical_problems_list
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    getter=technical_problem_getter,
    state=AdminBoilerDialog.admin_boiler_technical_problem_view,
    parse_mode=ParseMode.HTML
)

admin_boiler_technical_problem_create = Window(
    Format(
        text='✍️ <b>Введите название новой проблемы:</b>'
    ),
    Row(
        SwitchTo(
            id='back_to_new_fb_menu', text=Format('⬅️ Назад'), state=AdminBoilerDialog.admin_boiler_feedbacks_list
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=AdminBoilerDialog.admin_boiler_main_menu
        )
    ),
    MessageInput(new_technical_problem_name_handler),
    state=AdminBoilerDialog.admin_boiler_technical_problem_create_new,
    parse_mode=ParseMode.HTML
)


admin_boiler_dialog = Dialog(
    admin_boiler_main_menu,

    admin_boiler_feedbacks,
    admin_boiler_feedbacks_list,
    admin_boiler_feedback_view,

    admin_boiler_technical_problems_list,
    admin_boiler_technical_problem_view,
    admin_boiler_technical_problem_create
)
