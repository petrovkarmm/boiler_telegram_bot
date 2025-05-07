from aiogram_dialog import DialogManager

from db_configuration.crud import Feedback


async def feedback_count_getter(dialog_manager: DialogManager, **_kwargs):
    feedbacks = Feedback.get_all_unviewed_feedback()

    return {
        'feedbacks_count': len(feedbacks)
    }
