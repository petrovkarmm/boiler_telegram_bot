import operator

from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, ScrollingGroup, Column, Select, Counter, \
    Radio
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format

from main_menu.global_utils.global_messages_input import get_itn_and_organization_name

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_message_input_handlers import feedback_handler, \
    technical_problem_handler, technical_problem_description_handler, \
    handle_upload, address_getter, new_organization_itn_handler, new_phone_handler, new_organization_name_handler, \
    new_name_handler, budget_getter, place_format_getter, tech_catalog_address_getter
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_on_click_functions import send_feedback, \
    on_technical_problem_selected, confirm_sending_call_technician, get_barista_count_and_switch, \
    confirm_sending_barista_training, save_rent_and_switch, save_tech_cat_and_switch, save_barista_training_and_switch, \
    technical_catalog_radio_set, confirm_sending_tech_catalog_request, rent_radio_set, rent_catalog_radio_set, \
    confirm_rent_request_sending
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from main_menu.boiler_dialog.boiler_dialog_dataclasses import TECHNICAL_PROBLEM_KEY
from main_menu.boiler_dialog.boiler_dialog_getter import technical_problem_id_getter, technical_problems_getter, \
    user_data_profile_getter, user_data_profile_barista_getter, technical_catalog_getter, \
    get_technical_catalog_data_for_accept, \
    rent_type_getter, rent_data_for_accept_request, video_or_photo_format_data

boiler_main_menu = Window(
    Format(
        text='<b>Здравствуйте!</b>\n\n'
             '🧭 - В какой раздел сервиса вы хотите обратиться?'
    ),
    Row(
        SwitchTo(
            id='repair', text=Format('🛠️ Вызов техника'), state=BoilerDialog.boiler_repair_problem
        ),
        Button(
            id='rent', text=Format('📦 Аренда'), on_click=save_rent_and_switch
        ),
    ),
    Row(
        Button(
            id='tech_cat', text=Format('🔍 Подбор техники'), on_click=save_tech_cat_and_switch
        ),
        Button(
            id='bar_training', text=Format('☕ Обучение бариста'),
            on_click=save_barista_training_and_switch
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
        handle_upload
    ),
    getter=video_or_photo_format_data,
    state=BoilerDialog.boiler_repair_video_or_photo,
    parse_mode=ParseMode.HTML,
)

boiler_repair_address = Window(
    Format(
        text=(
            "📍 <b>Адрес и название заведения</b>\n\n"
            "Пожалуйста, укажите адрес, по которому требуется ремонт,\n"
            "а также название заведения.\n\n"
            "Пример:\n"
            "<i>г. Москва, ул. Ленина, д. 10, кафе «Уют»</i>"
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
    StaticMedia(path=Format("{dialog_data[tmp_file_path]}"), when=F['dialog_data']['tmp_file_path']),
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

boiler_rent_catalog_radio_get_set = Window(
    Format(
        text=(
            "🏠 <b>Аренда оборудования</b>\n\n"
            "Пожалуйста, выберите интересующий вас тип аренды:\n"
            "• <b>суточная</b> или <b>помесячная</b>?"
        )
    ),
    Radio(
        Format("🔘 {item[0]}"),
        Format("⚪️ {item[0]}"),
        id="rent_type",
        item_id_getter=operator.itemgetter(1),
        items="rents",
        on_state_changed=rent_radio_set,
    ),
    SwitchTo(
        id='ask_tech_type',
        text=Format(
            '➡️ Далее'
        ),
        when=F['dialog_data']['rent_type_radio_get_set'],
        state=BoilerDialog.boiler_rent_technical_type
    ),

    SwitchTo(
        id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
    ),
    getter=rent_type_getter,
    state=BoilerDialog.boiler_rent_type,
    parse_mode=ParseMode.HTML
)

boiler_rent_technical_type = Window(
    Format(
        text=(
            "🧰 <b>Подбор оборудования</b>\n\n"
            "Пожалуйста, выберите интересующий вас тип кофемашины:\n"
            "• <b>рожковая</b> или <b>автоматическая</b>?"
        )
    ),
    Radio(
        Format("🔘 {item[0]}"),
        Format("⚪️ {item[0]}"),
        id="rent_tech_type",
        item_id_getter=operator.itemgetter(1),
        items="catalog",
        on_state_changed=rent_catalog_radio_set,
    ),
    SwitchTo(
        id='ask_tech_type',
        text=Format(
            '➡️ Далее'
        ),
        when=F['dialog_data']['rent_catalog_radio_get_set'],
        state=BoilerDialog.boiler_rent_accept_request
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_rent_type
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    getter=technical_catalog_getter,
    state=BoilerDialog.boiler_rent_technical_type,
    parse_mode=ParseMode.HTML
)

boiler_rent_accept_request = Window(
    Format(
        text=(
            '✅ <b>{user_name}</b>, пожалуйста, проверьте все данные перед отправкой заявки:\n\n'
            '☕ <b>Тип кофемашины:</b> {user_technical_type}\n\n'
            '📦 <b>Тип аренды:</b> {user_rent_type}\n\n'
            '📞 <b>Телефон:</b> <i>{user_phone}</i>\n\n'
            '🏢 <b>Организация:</b> {organization_name}\n\n'
            '🧾 <b>ИНН:</b> {organization_itn}\n\n'
            'Если всё верно — нажмите <b>«Отправить»</b>.'
        )
    ),

    Button(
        id='send_rent_req', text=Format('📤 Отправить'), on_click=confirm_rent_request_sending
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_rent_technical_type
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    getter=rent_data_for_accept_request,
    state=BoilerDialog.boiler_rent_accept_request,
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

boiler_tech_catalog = Window(
    Format(
        text=(
            "🧰 <b>Подбор оборудования</b>\n\n"
            "Пожалуйста, выберите интересующий вас тип кофемашины:\n"
            "• <b>рожковая</b> или <b>автоматическая</b>?"
        )
    ),
    Radio(
        Format("🔘 {item[0]}"),
        Format("⚪️ {item[0]}"),
        id="tech_catalog",
        item_id_getter=operator.itemgetter(1),
        items="catalog",
        on_state_changed=technical_catalog_radio_set,
    ),
    SwitchTo(
        id='ask_budget',
        text=Format(
            '➡️ Далее'
        ),
        when=F['dialog_data']['technical_catalog_radio_get_set'],
        state=BoilerDialog.boiler_ask_budget
    ),
    SwitchTo(
        id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
    ),
    getter=technical_catalog_getter,
    state=BoilerDialog.boiler_technical_catalog_type_choose,
    parse_mode=ParseMode.HTML
)

boiler_ask_budget = Window(
    Format(
        "💰 <b>Бюджет</b>\n\n"
        "Пожалуйста, укажите, какой у вас бюджет на оборудование."
    ),
    MessageInput(
        budget_getter
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_technical_catalog_type_choose
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    state=BoilerDialog.boiler_ask_budget,
    parse_mode=ParseMode.HTML
)

boiler_ask_place_format = Window(
    Format(
        "🏪 <b>Формат заведения</b>\n\n"
        "Расскажите, пожалуйста, какой у вас формат заведения?\n"
        "Например: кафе, кофейня, ресторан и т.п."
    ),
    MessageInput(
        place_format_getter
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_ask_budget
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    state=BoilerDialog.boiler_ask_place_format,
    parse_mode=ParseMode.HTML
)

boiler_technical_address = Window(
    Format(
        text=(
            "📍 <b>Адрес и название заведения</b>\n\n"
            "Пожалуйста, укажите адрес,\n"
            "а также название заведения (если есть).\n\n"
            "Пример:\n"
            "<i>г. Москва, ул. Ленина, д. 10, кафе «Уют»</i>"
        )
    ),
    MessageInput(
        tech_catalog_address_getter
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_ask_place_format
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    state=BoilerDialog.boiler_tech_cat_address,
    parse_mode=ParseMode.HTML
)

boiler_accept_technical_request = Window(
    Format(
        text=(
            '✅ <b>{user_name}</b>, пожалуйста, проверьте все данные перед отправкой заявки на подбор техники:\n\n'
            '📍 <b>Адрес:</b> <i>{user_address}</i>\n\n'
            '🏷 <b>Тип кофемашины:</b> <i>{user_technical_type}</i>\n\n'
            '💰 <b>Бюджет:</b> <i>{user_budget}</i>\n\n'
            '🏬 <b>Формат заведения:</b> <i>{place_format}</i>\n\n'
            '📞 <b>Телефон:</b> <i>{user_phone}</i>\n\n'
            '🏢 <b>Организация:</b> <i>{organization_name}</i>\n\n'
            '🧾 <b>ИНН:</b> <i>{organization_itn}</i>\n\n'
            'Если всё верно — нажмите <b>«Отправить»</b>.'
        )
    ),
    Button(
        id='accept_rent_req', text=Format('📤 Отправить'), on_click=confirm_sending_tech_catalog_request
    ),
    Row(
        SwitchTo(
            id='back_to_t_pr', text=Format('⬅️ Назад'), state=BoilerDialog.boiler_tech_cat_address
        ),
        SwitchTo(
            id='back_to_menu', text=Format('🏠 В меню'), state=BoilerDialog.boiler_main_menu
        )
    ),
    getter=get_technical_catalog_data_for_accept,
    state=BoilerDialog.boiler_accept_tech_cat_request,
    parse_mode=ParseMode.HTML
)

task_waiting_window = Window(
    Format(
        'Идёт создание заявки. Пожалуйста, ожидайте.'
    ),
    state=BoilerDialog.boiler_send_task_waiting_status
)

upload_file_window = Window(
    Format(
        'Происходит отправка файла на сервер. Пожалуйста, подождите.'
    ),
    state=BoilerDialog.boiler_upload_file_waiting_status
)

boiler_dialog = Dialog(
    boiler_main_menu,

    boiler_tech_catalog,
    boiler_ask_budget,
    boiler_ask_place_format,
    boiler_technical_address,
    boiler_accept_technical_request,

    boiler_rent_catalog_radio_get_set,
    boiler_rent_technical_type,
    boiler_rent_accept_request,

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
    boiler_barista_training_accept_request,

    task_waiting_window,
    upload_file_window
)
