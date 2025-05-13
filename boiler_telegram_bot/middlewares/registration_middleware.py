from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from aiogram_dialog import DialogManager

from db_configuration.models.user import User
from main_menu.boiler_registration_dialog.boiler_registration_states import BoilerRegistrationDialog


class UserInDatabaseChecker(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        dialog_manager = data["dialog_manager"]
        current_update_data = data["event_update"]
        dialog_manager: DialogManager

        user_id = current_update_data.message.from_user.id

        user_status_in_database = User.check_user_in_database(user_id)

        if user_status_in_database:
            result = await handler(event, data)
            return result
        else:
            await dialog_manager.start(
                BoilerRegistrationDialog.boiler_registration_user_name
            )
