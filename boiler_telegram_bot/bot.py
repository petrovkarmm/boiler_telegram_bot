import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from boiler_telegram_bot.keyboards import repair_bot_keyboard
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_router import boiler_dialog_router
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from boiler_telegram_bot.main_menu.main_menu_router import main_menu_router
from boiler_telegram_bot.cleanup_tmp import cleanup_tmp_files
from boiler_telegram_bot.db_configuration.create_tables import create_tables
from boiler_telegram_bot.db_configuration.models.user import User
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_router import admin_boiler_dialog_router
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_states import AdminBoilerDialog
from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_router import \
    boiler_registration_dialog_router
from boiler_telegram_bot.main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog
from boiler_telegram_bot.middlewares.logger_middleware import GlobalLogger
from boiler_telegram_bot.settings import bot_token, DEBUG, redis_connect_url, admin_panel_password
from boiler_telegram_bot.tg_logs.logger import bot_logger
from boiler_telegram_bot.db_configuration.insert_values_in_db import insert_values


async def bot_start():
    if DEBUG:
        dp = Dispatcher()
    else:
        storage = RedisStorage.from_url(
            redis_connect_url, key_builder=DefaultKeyBuilder(with_destiny=True)
        )
        dp = Dispatcher(storage=storage)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(cleanup_tmp_files, trigger="cron", hour=3)
    scheduler.start()

    bot = Bot(token=bot_token)

    setup_dialogs(dp)

    @dp.message(Command(admin_panel_password))
    async def admin_panel_start(message: Message, state: FSMContext, dialog_manager: DialogManager):
        await dialog_manager.start(
            AdminBoilerDialog.admin_boiler_main_menu
        )

    @dp.message(F.text == '🏪 Перезапустить бота')
    async def repair_bot(message: Message, state: FSMContext, dialog_manager: DialogManager):
        user_id = message.from_user.id

        user_status_in_database = User.check_user_in_database(user_id)

        if user_status_in_database:
            await message.answer(
                text='🔄 <b>Перезапускаемся...</b> 🚀',
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=ParseMode.HTML
            )

            await dialog_manager.start(
                BoilerDialog.boiler_main_menu,
                data={'user_id': message.from_user.id},
            )
        else:
            await message.answer(
                text='⚠️ Упс! Кажется, что-то пошло не так.',
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=ParseMode.HTML
            )

            await dialog_manager.start(
                BoilerRegistrationDialog.boiler_registration_user_name
            )

    async def error_unknown_intent_handler(
            event: ErrorEvent, dialog_manager: DialogManager
    ):
        if isinstance(event.exception, UnknownIntent) or isinstance(event.exception, OutdatedIntent):
            try:
                event_message_id = event.update.callback_query.message.message_id
                event_chat_id = event.update.callback_query.message.chat.id
                await bot.delete_message(
                    chat_id=event_chat_id, message_id=event_message_id
                )
                await bot.send_message(
                    text='⚠️ Упс! Кажется, что-то пошло не так. Чтобы перезапустить бота, нажмите кнопку под чатом. 🔄',
                    reply_markup=repair_bot_keyboard(),
                    chat_id=event_chat_id,
                    parse_mode=ParseMode.HTML
                )
            except AttributeError as exception:
                bot_logger.warning(f'Отбилась в закрытый диалог.', exception)
            except Exception as exception:
                bot_logger.warning(exception)
        else:
            bot_logger(f"{event.exception}")

    # error handler
    dp.errors.register(error_unknown_intent_handler)

    # logger mw
    dp.callback_query.middleware.register(GlobalLogger())

    # dialogs
    dp.include_router(
        boiler_registration_dialog_router
    )
    dp.include_router(
        boiler_dialog_router
    )
    dp.include_router(
        admin_boiler_dialog_router
    )

    # handlers
    dp.include_router(
        main_menu_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        bot_logger.info(
            'Старт бота.'
        )
        create_tables()
        insert_values()
        asyncio.run(bot_start())
    except Exception as e:
        bot_logger.warning(e)
