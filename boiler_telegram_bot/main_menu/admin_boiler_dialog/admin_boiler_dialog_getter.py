from datetime import datetime

from aiogram_dialog import DialogManager

from boiler_telegram_bot.db_configuration.models.technical_problem import TechnicalProblem
from boiler_telegram_bot.db_configuration.models.feedback import Feedback
from boiler_telegram_bot.main_menu.admin_boiler_dialog.admin_boiler_dialog_dataclasses import AdminFeedbackDialog, ADMIN_FEEDBACK_KEY, \
    ADMIN_TECHNICAL_PROBLEM_KEY, AdminTechnicalProblemDialog


async def feedbacks_count_getter(dialog_manager: DialogManager, **_kwargs):
    new_feedbacks = Feedback.get_all_unviewed_feedback()
    old_feedbacks = Feedback.get_all_viewed_feedback()

    new_feedbacks_count = len(new_feedbacks)
    old_feedbacks_count = len(old_feedbacks)

    return {
        'new_feedbacks_count': new_feedbacks_count,
        'old_feedbacks_count': old_feedbacks_count
    }


async def technical_problem_getter(dialog_manager: DialogManager, **_kwargs):
    technical_problem_id = dialog_manager.dialog_data['technical_problem_id']

    technical_problem = TechnicalProblem.get_technical_problem_by_id(technical_problem_id=technical_problem_id)

    technical_problem_name = technical_problem['name']
    technical_problem_hidden = 'Скрыт' if technical_problem['hidden'] == 1 else 'Отображается'
    technical_problem_created = technical_problem['created']
    technical_problem_updated = technical_problem['updated']

    technical_problem_created_dt = datetime.strptime(technical_problem_created, "%Y-%m-%d %H:%M:%S")
    technical_problem_created_formatted = technical_problem_created_dt.strftime("%d.%m.%Y %H:%M:%S")

    technical_problem_updated_dt = datetime.strptime(technical_problem_updated, "%Y-%m-%d %H:%M:%S")
    technical_problem_updated_formatted = technical_problem_updated_dt.strftime("%d.%m.%Y %H:%M:%S")

    return {
        'technical_problem_name': technical_problem_name,
        'technical_problem_hidden': technical_problem_hidden,
        'technical_problem_created': technical_problem_created_formatted,
        'technical_problem_updated': technical_problem_updated_formatted
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


def feedback_id_getter(feedback: AdminFeedbackDialog) -> int:
    return feedback.id


def technical_problem_id_getter(technical_problem: AdminTechnicalProblemDialog) -> int:
    return technical_problem.id


async def feedbacks_getter(dialog_manager: DialogManager, **_kwargs):
    menu_status = dialog_manager.dialog_data['feedback_menu']

    if menu_status == 'new':

        feedbacks = Feedback.get_all_unviewed_feedback()
        feedbacks_count = len(feedbacks)

        return {
            ADMIN_FEEDBACK_KEY: [
                AdminFeedbackDialog(
                    new_feedback["id"],
                    AdminFeedbackDialog.formatted_feedback_text(
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
            ADMIN_FEEDBACK_KEY: [
                AdminFeedbackDialog(
                    new_feedback["id"],
                    AdminFeedbackDialog.formatted_feedback_text(
                        new_feedback["feedback_text"]
                    )
                )
                for new_feedback in feedbacks
            ],
            'new_feedbacks_count': feedbacks_count
        }


async def technical_problems_getter(dialog_manager: DialogManager, **_kwargs):
    technical_problems = TechnicalProblem.get_all_technical_problem()

    return {
        ADMIN_TECHNICAL_PROBLEM_KEY: [
            AdminTechnicalProblemDialog(
                id=technical_problem["id"],
                name=AdminTechnicalProblemDialog.formatted_hidden_problems(
                    name=technical_problem['name'],
                    hidden=technical_problem['hidden']
                )
            )
            for technical_problem in technical_problems
        ]
    }
