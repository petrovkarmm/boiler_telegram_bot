from aiogram_dialog import DialogManager

from db_configuration.crud import Feedback
from main_menu.admin_boiler_dialog.admin_boiler_dialog_dataclasses import FeedbackDialog, FEEDBACK_KEY


async def feedback_count_getter(dialog_manager: DialogManager, **_kwargs):
    feedbacks = Feedback.get_all_unviewed_feedback()

    return {
        'feedbacks_count': len(feedbacks)
    }


def feedback_id_getter(feedback: FeedbackDialog) -> int:
    return feedback.id


async def new_feedbacks_getter(**_kwargs):
    new_feedbacks = Feedback.get_all_unviewed_feedback()

    return {
        FEEDBACK_KEY: [
            FeedbackDialog(
                new_feedback["id"],
                FeedbackDialog.formatted_feedback_text(
                    new_feedback["feedback_text"]
                )
            )
            for new_feedback in new_feedbacks
        ]
    }
