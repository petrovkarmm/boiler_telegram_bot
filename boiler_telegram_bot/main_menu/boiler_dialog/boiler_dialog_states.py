from aiogram.fsm.state import StatesGroup, State


class BoilerDialog(StatesGroup):
    boiler_main_menu = State()

    boiler_feedback = State()
    boiler_accept_feedback = State()

    boiler_repair_problem = State()
    boiler_repair_description = State()
    boiler_repair_video_or_photo = State()
    boiler_repair_name = State()
    boiler_repair_phone = State()
    boiler_repair_accept_request = State()

    boiler_technical_catalog_type_choose = State()

    boiler_rent = State()

    boiler_barista_training_choose_count = State()
    boiler_barista_training_get_itn_and_org_name = State()
    boiler_barista_training_accept_request = State()
