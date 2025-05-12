from aiogram.fsm.state import StatesGroup, State


class AdminBoilerDialog(StatesGroup):
    admin_boiler_main_menu = State()

    admin_boiler_feedbacks_menu = State()
    admin_boiler_feedbacks_list = State()
    admin_boiler_feedback_view = State()

    admin_boiler_technical_problems_list = State()
    admin_boiler_technical_problem_view = State()
