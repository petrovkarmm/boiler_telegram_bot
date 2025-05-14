from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select, Counter
from aiogram_dialog.widgets.text import Format

from main_menu.global_utils.global_messages_input import get_itn_and_organization_name

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_message_input_handlers import feedback_handler, \
    technical_problem_handler, technical_problem_description_handler, \
    content_handler, address_getter, new_organization_itn_handler, new_phone_handler, new_organization_name_handler, \
    new_name_handler
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_on_click_functions import send_feedback, \
    on_technical_problem_selected, confirm_sending_call_technician, get_barista_count_and_switch, \
    confirm_sending_barista_training
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from main_menu.boiler_dialog.boiler_dialog_dataclasses import TECHNICAL_PROBLEM_KEY
from main_menu.boiler_dialog.boiler_dialog_getter import technical_problem_id_getter, technical_problems_getter, \
    user_data_profile_getter, user_data_profile_barista_getter

boiler_main_menu = Window(
    Format(
        text='<b>Здравствуйте!</b>\n\n'
             '🧭 - В какой раздел сервиса вы хотите обратиться?'
    ),
    Row(
        SwitchTo(
            id='repair', text=Format('🛠️ Вызов техника'), state=BoilerDialog.boiler_repair_problem
        ),
        SwitchTo(
            id='rent', text=Format('🏢 Аренда'), state=BoilerDialog.boiler_rent
        ),
    ),
    Row(
        SwitchTo(
            id='tech_cat', text=Format('📦 Подбор техники'), state=BoilerDialog.boiler_technical_catalog_type_choose
        ),
        SwitchTo(
            id='bar_training', text=Format('☕ Обучение бариста'),
            state=BoilerDialog.boiler_barista_training_choose_count
        ),
    ),
    SwitchTo(
        id='profile_edit', text=Format('📝 Редактирование профиля'), state=BoilerDialog.boiler_profile_edit_menu
    ),
    SwitchTo(
        id='text_back', text=Format('💬 Обратная связь'), state=BoilerDialog.boiler_feedback
    ),
    state=BoilerDialog.boiler_main_menu,
    parse_mode=ParseMode.HTML
)

boiler_profile_edit_menu = Window(
    Format(
        text="Выберите, что отредактировать: \n\n"
             "👤 <b>Имя пользователя:</b> {user_name}\n\n"
             '📞 <b>Телефон:</b> {user_phone}\n\n'
             "🏢 <b>Организация:</b> {organization_name}\n\n"
             "🧾 <b>ИНН:</b> {organization_itn}\n\n"

    ),
    Row(
        SwitchTo(
            id='edit_name', text=Format('👤 Имя'), state=BoilerDialog.boiler_profile_edit_name
        ),
        SwitchTo(
            id='edit_phone', text=Format('📞 Телефон'), state=BoilerDialog.boiler_profile_edit_phone
        )
    ),
    Row(
        SwitchTo(
            id='edit_o_name', text=Format('🏢 Организация'), state=BoilerDialog.boiler_profile_edit_organization_name
        ),
        SwitchTo(
            id='edit_itn', text=Format('🧾 ИНН'), state=BoilerDialog.boiler_profile_edit_organization_itn
        ),
    ),
    SwitchTo(
        id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
    ),
    getter=user_data_profile_getter,
    state=BoilerDialog.boiler_profile_edit_menu,
    parse_mode=ParseMode.HTML
)

boiler_profile_edit_itn = Window(
    Format(
        text=(
            "🧾 <b>ИНН организации</b>\n\n"
            "Пожалуйста, введите новое значение ИНН вашей организации:"
        )
    ),
    Row(
        SwitchTo(
            id='back_to_feedback', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_profile_edit_menu
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        ),
    ),
    MessageInput(
        new_organization_itn_handler
    ),
    state=BoilerDialog.boiler_profile_edit_organization_itn,
    parse_mode=ParseMode.HTML
)

boiler_profile_edit_phone = Window(
    Format(
        text=(
            "📞 <b>Номер телефона</b>\n\n"
            "Пожалуйста, укажите новый номер для связи с вами.\n"
            "Допустимый формат: <b>+7XXXXXXXXXX</b> или <b>8XXXXXXXXXX</b>\n\n"
            "Убедитесь, что номер введён корректно — мы свяжемся с вами по нему."
        )
    ),
    Row(
        SwitchTo(
            id='back_to_feedback', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_profile_edit_menu
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        ),
    ),
    MessageInput(
        new_phone_handler
    ),
    state=BoilerDialog.boiler_profile_edit_phone,
    parse_mode=ParseMode.HTML
)

boiler_profile_edit_organization_name = Window(
    Format(
        text=(
            "🏢 <b>Название организации</b>\n\n"
            "Введите, пожалуйста, новое название вашей организации:"
        )
    ),
    MessageInput(
        new_organization_name_handler
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_profile_edit_menu
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        ),
    ),
    state=BoilerDialog.boiler_profile_edit_organization_name,
    parse_mode=ParseMode.HTML
)

boiler_profile_edit_name = Window(
    Format(
        text=(
            "🙋‍♂️ Пожалуйста, напишите, как к вам можно обращаться (ваше имя):"
        )
    ),
    MessageInput(
        new_name_handler
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_profile_edit_menu
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        ),
    ),
    state=BoilerDialog.boiler_profile_edit_name,
    parse_mode=ParseMode.HTML
)

boiler_feedback = Window(
    Format(
        '💬 <b>Обратная связь</b>\n\n'
        '📩 Отправьте в этот чат сообщение с вашей обратной связью, '
        'и мы обязательно передадим его нашим специалистам.\n\n'
        '🙏 Спасибо за помощь в улучшении нашего сервиса!'
    ),
    MessageInput(
        feedback_handler
    ),
    SwitchTo(
        id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
    ),
    state=BoilerDialog.boiler_feedback,
    parse_mode=ParseMode.HTML
)

boiler_accept_feedback = Window(
    Format(
        text=(
            '📝 <b>Вы написали:</b>\n\n'
            '<i>{dialog_data[user_answer]}</i>'
        )
    ),
    Button(
        id='send_feedback',
        text=Format('📤 Отправить'),
        on_click=send_feedback
    ),
    Row(
        SwitchTo(
            id='back_to_feedback', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_feedback
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        ),
    ),
    state=BoilerDialog.boiler_accept_feedback,
    parse_mode=ParseMode.HTML,
)

boiler_repair_problem = Window(
    Format(
        text=(
            '🛠 <b>Выбор темы проблемы</b>\n\n'
            '🔽 Выберите тему из списка ниже.\n'
            'Если нужной темы нет — просто отправьте сообщение с описанием проблемы в чат 👇'
        )
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format("{item.name}"),
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
        id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
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
        text=(
            '📝 <b>Тема проблемы:</b> <i>{dialog_data[technical_problem]}</i>\n\n'
            '📌 Пожалуйста, опишите проблему максимально подробно.'
        )
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_repair_problem
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    MessageInput(
        technical_problem_description_handler
    ),
    state=BoilerDialog.boiler_repair_description,
    parse_mode=ParseMode.HTML,
)

boiler_repair_boiler_video_or_photo = Window(
    Format(
        text=(
            '📌 <b>Тема проблемы:</b> <i>{dialog_data[technical_problem]}</i>\n\n'
            '📝 <b>Описание:</b> <i>{dialog_data[technical_problem_description]}</i>\n\n'
            '📷 При необходимости прикрепите фото или видео, чтобы нам было проще разобраться.\n'
            'Если медиа нет — просто нажмите "Далее".'
        )
    ),
    SwitchTo(
        id='skip_step', text=Format('➡️ Далее'), state=BoilerDialog.boiler_repair_address
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_repair_description
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    MessageInput(
        content_handler
    ),
    state=BoilerDialog.boiler_repair_video_or_photo,
    parse_mode=ParseMode.HTML,
)

boiler_repair_address = Window(
    Format(
        text=(
            "📍 <b>Адрес</b>\n\n"
            "Пожалуйста, укажите адрес, по которому требуется ремонт:"
        )
    ),
    MessageInput(
        address_getter
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_repair_video_or_photo
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    state=BoilerDialog.boiler_repair_address,
    parse_mode=ParseMode.HTML
)

boiler_repair_accept_request = Window(
    Format(
        text=(
            '✅ <b>{user_name}</b>, пожалуйста, проверьте все данные перед отправкой заявки:\n\n'
            '📌 <b>Тема проблемы:</b> <i>{dialog_data[technical_problem]}</i>\n\n'
            '📝 <b>Описание:</b> <i>{dialog_data[technical_problem_description]}</i>\n\n'
            '🏘 <b>Адрес:</b> <i>{dialog_data[user_address]}</i>\n\n'
            '📞 <b>Телефон:</b> <i>{user_phone}</i>\n\n'
            "🏢 <b>Организация:</b> {organization_name}\n\n"
            "🧾 <b>ИНН:</b> {organization_itn}\n\n"
            'Если всё верно — нажмите <b>«Отправить»</b>.'
        )
    ),
    Button(
        id='accept_rp_rq', text=Format('📤 Отправить'), on_click=confirm_sending_call_technician
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_repair_address
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    getter=user_data_profile_getter,
    state=BoilerDialog.boiler_repair_accept_request,
    parse_mode=ParseMode.HTML,
)

boiler_technical_catalog_type_choose = Window(
    Format(
        text='Выбор типа техники test'
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_repair_video_or_photo
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    state=BoilerDialog.boiler_technical_catalog_type_choose,
    parse_mode=ParseMode.HTML
)

boiler_barista_training_choose_count = Window(
    Format(
        text='Подскажите, сколько человек планируете обучить?'
    ),
    Counter(
        id="barista_counter",
        text=Format(
            '{value:g}'
        ),
        default=1,
        max_value=100,
        on_text_click=None,
        plus=Format(
            '➕'
        ),
        minus=Format(
            '➖'
        )
    ),
    Button(
        id='accept_count', text=Format('✅ Подтвердить'), on_click=get_barista_count_and_switch
    ),
    SwitchTo(
        id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
    ),
    state=BoilerDialog.boiler_barista_training_choose_count,
    parse_mode=ParseMode.HTML
)

boiler_barista_training_accept_request = Window(
    Format(
        text=(
            '✅ <b>{user_name}</b>, пожалуйста, проверьте все данные перед отправкой заявки:\n\n'
            '📌 <b>Кол-во человек на обучение:</b> <i>{barista_value}</i>\n\n'
            '📞 <b>Телефон:</b> <i>{user_phone}</i>\n\n'
            "🏢 <b>Организация:</b> {organization_name}\n\n"
            "🧾 <b>ИНН:</b> {organization_itn}\n\n"
            'Если всё верно — нажмите <b>«Отправить»</b>.'
        )
    ),
    Button(
        id='accept_br_req', text=Format('📤 Отправить'), on_click=confirm_sending_barista_training
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_barista_training_choose_count
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    getter=user_data_profile_barista_getter,
    state=BoilerDialog.boiler_barista_training_accept_request,
    parse_mode=ParseMode.HTML
)

boiler_dialog = Dialog(
    boiler_main_menu,

    boiler_profile_edit_menu,
    boiler_profile_edit_itn,
    boiler_profile_edit_name,
    boiler_profile_edit_phone,
    boiler_profile_edit_organization_name,

    boiler_feedback,
    boiler_accept_feedback,

    boiler_repair_problem,
    boiler_repair_description,
    boiler_repair_boiler_video_or_photo,
    boiler_repair_address,
    boiler_repair_accept_request,

    boiler_barista_training_choose_count,
    boiler_barista_training_accept_request
)
