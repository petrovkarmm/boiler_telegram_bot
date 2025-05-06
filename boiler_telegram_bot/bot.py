import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent
from dotenv import load_dotenv, find_dotenv

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_router import boiler_dialog_router
from boiler_telegram_bot.main_menu.main_menu_router import main_menu_router

load_dotenv(find_dotenv())

token = os.getenv("BOT_TOKEN")


async def bot_start():
    # main configuration
    bot = Bot(token=token)
    dp = Dispatcher()
    setup_dialogs(dp)

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
            except AttributeError:
                print(f'Отбилась в закрытый диалог.')
            except Exception as exception:
                print(exception)

        else:
            return print(f"{event}")

    # error handler
    # dp.errors.register(error_unknown_intent_handler)

    # dialogs
    dp.include_router(
        boiler_dialog_router
    )

    # handlers
    dp.include_router(
        main_menu_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(bot_start())
    except Exception as e:
        print(e)
