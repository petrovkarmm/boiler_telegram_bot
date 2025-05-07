from aiogram.fsm.state import StatesGroup, State


class BoilerDialog(StatesGroup):
    boiler_main_menu = State()

    boiler_feedback = State()
    boiler_accept_feedback = State()

    boiler_repair_problem = State()
    boiler_repair_description = State()

    boiler_technical_catalog = State()

    boiler_rent = State()

    boiler_barista_training = State()
