from datetime import datetime

from aiogram_dialog import DialogManager

from db_configuration.crud import Feedback
from main_menu.admin_boiler_dialog.admin_boiler_dialog_dataclasses import FeedbackDialog, FEEDBACK_KEY


async def feedbacks_count_getter(dialog_manager: DialogManager, **_kwargs):
    new_feedbacks = Feedback.get_all_unviewed_feedback()
    old_feedbacks = Feedback.get_all_viewed_feedback()

    new_feedbacks_count = len(new_feedbacks)
    old_feedbacks_count = len(old_feedbacks)

    return {
        'new_feedbacks_count': new_feedbacks_count,
        'old_feedbacks_count': old_feedbacks_count
    }


async def feedback_getter(dialog_manager: DialogManager, **_kwargs):
    feedback_id = dialog_manager.dialog_data['feedback_id']

    feedback = Feedback.get_feedback_by_id(feedback_id=feedback_id)

    tg_user_id = feedback['tg_user_id']
    user_firstname = feedback['user_firstname']
    user_lastname = feedback['user_lastname']
    user_username = feedback['user_username']
    feedback_text = feedback['feedback_text']
    created = feedback['created']

    created_dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
    created_formatted = created_dt.strftime("%d.%m.%Y %H:%M:%S")

    return {
        "tg_user_id": tg_user_id,
        "user_firstname": user_firstname,
        "user_lastname": user_lastname,
        "user_username": user_username,
        "feedback_text": feedback_text,
        "created": created_formatted
    }


def feedback_id_getter(feedback: FeedbackDialog) -> int:
    return feedback.id


async def feedbacks_getter(dialog_manager: DialogManager, **_kwargs):
    menu_status = dialog_manager.dialog_data['feedback_menu']

    if menu_status == 'new':

        feedbacks = Feedback.get_all_unviewed_feedback()
        feedbacks_count = len(feedbacks)

        return {
            FEEDBACK_KEY: [
                FeedbackDialog(
                    new_feedback["id"],
                    FeedbackDialog.formatted_feedback_text(
                        new_feedback["feedback_text"]
                    )
                )
                for new_feedback in feedbacks
            ],
            'new_feedbacks_count': feedbacks_count
        }

    else:

        feedbacks = Feedback.get_all_viewed_feedback()
        feedbacks_count = len(feedbacks)

        return {
            FEEDBACK_KEY: [
                FeedbackDialog(
                    new_feedback["id"],
                    FeedbackDialog.formatted_feedback_text(
                        new_feedback["feedback_text"]
                    )
                )
                for new_feedback in feedbacks
            ],
            'new_feedbacks_count': feedbacks_count
        }
