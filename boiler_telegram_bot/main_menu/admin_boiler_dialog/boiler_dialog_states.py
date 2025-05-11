from aiogram.fsm.state import StatesGroup, State


class AdminBoilerDialog(StatesGroup):
    admin_boiler_main_menu = State()
    admin_boiler_technical_problems = State()

    admin_boiler_feedbacks_menu = State()
    admin_boiler_feedbacks_list = State()

    admin_boiler_feedback_view = State()
