import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent

from boiler_telegram_bot.keyboards import repair_bot_keyboard
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_router import boiler_dialog_router
from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog_states import BoilerDialog
from boiler_telegram_bot.main_menu.main_menu_router import main_menu_router
from main_menu.admin_boiler_dialog.admin_boiler_dialog_router import admin_boiler_dialog_router
from main_menu.admin_boiler_dialog.admin_boiler_dialog_states import AdminBoilerDialog
from settings import bot_token, DEBUG


async def bot_start():
    # main configuration
    if DEBUG:
        bot = Bot(token=bot_token)
        dp = Dispatcher()
        setup_dialogs(dp)
    else:
        bot = Bot(token=bot_token)
        dp = Dispatcher()
        setup_dialogs(dp)

    @dp.message(F.text == 'admin_test')
    async def admin_panel_start(message: Message, state: FSMContext, dialog_manager: DialogManager):
        await dialog_manager.start(
            AdminBoilerDialog.admin_boiler_main_menu
        )

    @dp.message(F.text == '🏪 Перезапустить бота')
    async def repair_bot(message: Message, state: FSMContext, dialog_manager: DialogManager):
        await message.answer(
            text='Перезапускаемся. . .',
            reply_markup=ReplyKeyboardRemove()
        )

        await dialog_manager.start(
            BoilerDialog.boiler_main_menu,
            data={'user_id': message.from_user.id},
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
                    text='Упс. Кажется что-то пошло не так. Чтобы перезапустить бота нажмите кнопку под чатом. ',
                    reply_markup=repair_bot_keyboard(),
                    chat_id=event_chat_id
                )
            except AttributeError as exception:
                print(f'Отбилась в закрытый диалог.', exception)
            except Exception as exception:
                print(exception)

        else:
            return print(f"{event.exception}")

    # error handler
    dp.errors.register(error_unknown_intent_handler)

    # dialogs
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
        asyncio.run(bot_start())
    except Exception as e:
        print(e)
