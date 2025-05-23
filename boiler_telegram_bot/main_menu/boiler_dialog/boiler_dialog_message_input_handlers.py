import tempfile
import uuid
import os

from aiogram.enums import ParseMode
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from db_configuration.models.user import User
from main_menu.boiler_dialog.utils import normalize_phone_number, download_file
from main_menu.boiler_registration_dialog.utils import is_valid_inn


async def feedback_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_answer = message.text
    if user_answer:
        if len(user_answer) > 1000:
            await message.answer(
                text=(
                    "⚠️ <b>Ответ слишком длинный!</b>\n\n"
                    "Максимальная длина — <b>1000 символов</b>.\n"
                    "Пожалуйста, сократите текст и попробуйте ещё раз ✂️"
                ),
            )
        else:
            dialog_manager.dialog_data['user_answer'] = user_answer
            await dialog_manager.switch_to(
                BoilerDialog.boiler_accept_feedback
            )
    else:
        await message.answer(
            text='🤔 Похоже, вы отправили что-то не то...'
        )


async def technical_problem_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_technical_problem = message.text
    if user_technical_problem:
        if len(user_technical_problem) >= 100:
            await message.answer(
                text=(
                    "⚠️ <b>Тема проблемы слишком длинная!</b>\n\n"
                    "Максимальная длина — <b>100 символов</b>.\n"
                    "Пожалуйста, сократите текст и попробуйте ещё раз ✂️"
                ),
            )
        else:
            dialog_manager.dialog_data['technical_problem'] = user_technical_problem
            await dialog_manager.switch_to(
                BoilerDialog.boiler_repair_description
            )
    else:
        await message.answer(
            text='🤔 Похоже, вы отправили что-то не то...'
        )


async def technical_problem_description_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_technical_problem_description = message.text
    if user_technical_problem_description:
        if len(user_technical_problem_description) >= 2000:
            await message.answer(
                text=(
                    "⚠️ <b>Описание слишком длинное!</b>\n\n"
                    "Максимальная длина — <b>2000 символов</b>.\n"
                    "Пожалуйста, сократите текст и попробуйте ещё раз ✂️"
                ),
                parse_mode=ParseMode.HTML
            )
        else:
            dialog_manager.dialog_data['technical_problem_description'] = user_technical_problem_description
            await dialog_manager.switch_to(
                BoilerDialog.boiler_repair_video_or_photo
            )
    else:
        await message.answer(
            text='🤔 Похоже, вы отправили что-то не то...'
        )


async def new_organization_itn_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    inn = message.text.strip()

    if not is_valid_inn(inn):
        await message.answer("❌ Неверный ИНН. Пожалуйста, введите корректный ИНН из 10 или 12 цифр.")
        return

    telegram_id = str(message.from_user.id)

    User.update_user_field(
        telegram_id=telegram_id, key='organization_itn', new_value=inn
    )

    await dialog_manager.switch_to(
        BoilerDialog.boiler_profile_edit_menu
    )


async def new_organization_name_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    telegram_id = str(message.from_user.id)
    new_organization_name = message.text

    User.update_user_field(
        telegram_id=telegram_id,
        key='organization_name',
        new_value=new_organization_name
    )

    await dialog_manager.switch_to(
        BoilerDialog.boiler_profile_edit_menu
    )


async def new_name_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    telegram_id = str(message.from_user.id)
    new_name = message.text

    User.update_user_field(
        telegram_id=telegram_id,
        key='name',
        new_value=new_name
    )

    await dialog_manager.switch_to(
        BoilerDialog.boiler_profile_edit_menu
    )


async def new_phone_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_phone = message.text

    validate_user_phone = await normalize_phone_number(
        user_phone
    )

    if validate_user_phone:

        telegram_id = str(message.from_user.id)

        User.update_user_field(
            telegram_id=telegram_id, key='phone', new_value=user_phone
        )

        await dialog_manager.switch_to(
            BoilerDialog.boiler_profile_edit_menu
        )

    else:
        await message.answer(
            text="❌ <b>Некорректный номер телефона</b>\n\n"
                 "Пожалуйста, введите номер в одном из следующих форматов:\n"
                 "📱 <code>+7XXXXXXXXXX</code> или <code>8XXXXXXXXXX</code>\n\n"
                 "Попробуйте ещё раз 👇",
            parse_mode=ParseMode.HTML
        )


async def handle_upload(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    media = message.video or (message.photo[-1] if message.photo else None)
    await dialog_manager.switch_to(
        BoilerDialog.boiler_upload_file_waiting_status
    )
    try:
        if not media:
            await message.answer("Нет файла для загрузки.")
            return

        file_id = media.file_id
        file_bytes = await download_file(message.bot, file_id, message)
        if not file_bytes:
            return

        # Определим расширение файла
        if hasattr(media, "file_name") and media.file_name:
            ext = os.path.splitext(media.file_name)[1] or ".dat"
        elif message.video:
            ext = ".mp4"
        elif message.photo:
            ext = ".jpg"
        else:
            ext = ".dat"

        # Генерируем уникальное имя и путь
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        tmp_dir = tempfile.gettempdir()  # кросс-платформенный tmp путь
        tmp_file_path = os.path.join(tmp_dir, unique_filename)

        # Сохраняем файл
        with open(tmp_file_path, "wb") as tmp_file:
            tmp_file.write(file_bytes)

        dialog_manager.dialog_data["tmp_file_path"] = tmp_file_path
        dialog_manager.dialog_data["filename"] = unique_filename
    except Exception as e:
        await message.answer(
            text=(
                "❌ <b>Кажется, что-то пошло не так...</b>\n\n"
                "Пожалуйста, попробуйте ещё раз 🔄\n"
                "Если проблема не исчезнет, сообщите нам! 💬"
            ),
            parse_mode=ParseMode.HTML
        )
        await dialog_manager.switch_to(
            BoilerDialog.boiler_repair_video_or_photo
        )

    await dialog_manager.switch_to(
        BoilerDialog.boiler_repair_address
    )


async def address_getter(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_address = message.text

    dialog_manager.dialog_data['user_address'] = user_address

    await dialog_manager.switch_to(
        BoilerDialog.boiler_repair_accept_request
    )


async def tech_catalog_address_getter(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_address = message.text

    dialog_manager.dialog_data['user_address'] = user_address

    await dialog_manager.switch_to(
        BoilerDialog.boiler_accept_tech_cat_request
    )


async def budget_getter(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    user_budget = message.text

    dialog_manager.dialog_data['user_budget'] = user_budget

    await dialog_manager.switch_to(
        BoilerDialog.boiler_ask_place_format
    )


async def place_format_getter(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    place_format = message.text

    dialog_manager.dialog_data['place_format'] = place_format

    await dialog_manager.switch_to(
        BoilerDialog.boiler_tech_cat_address
    )
