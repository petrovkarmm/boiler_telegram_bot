from aiogram.fsm.state import StatesGroup, State


class BoilerDialog(StatesGroup):
    boiler_main_menu = State()
    boiler_feedback = State()
    boiler_accept_feedback = State()

    boiler_repair_menu = State()
