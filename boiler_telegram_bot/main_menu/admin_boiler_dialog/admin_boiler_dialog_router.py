from aiogram import Router

from main_menu.admin_boiler_dialog.admin_boiler_dialog import admin_boiler_dialog

admin_boiler_dialog_router = Router()

admin_boiler_dialog_router.include_router(admin_boiler_dialog)
