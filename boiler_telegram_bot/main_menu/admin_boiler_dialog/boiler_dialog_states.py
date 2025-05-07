from aiogram.fsm.state import StatesGroup, State


class AdminBoilerDialog(StatesGroup):
    admin_boiler_main_menu = State()
    admin_boiler_feedbacks = State()
    admin_boiler_technical_problems = State()
