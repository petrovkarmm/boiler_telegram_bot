from aiogram import Router

from boiler_telegram_bot.main_menu.boiler_dialog.boiler_dialog import boiler_dialog

boiler_dialog_router = Router()

boiler_dialog_router.include_router(boiler_dialog)
