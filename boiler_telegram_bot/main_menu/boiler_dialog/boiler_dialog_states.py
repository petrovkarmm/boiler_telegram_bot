from aiogram.fsm.state import StatesGroup, State


class BoilerDialog(StatesGroup):
    boiler_main_menu = State()

    boiler_profile_edit_menu = State()
    boiler_profile_edit_name = State()
    boiler_profile_edit_phone = State()
    boiler_profile_edit_organization_itn = State()
    boiler_profile_edit_organization_name = State()

    boiler_profile_create_new_individual_name = State()
    boiler_profile_create_new_individual_phone = State()
    boiler_profile_accept_new_individual_profile = State()

    boiler_feedback = State()
    boiler_accept_feedback = State()

    boiler_repair_problem = State()
    boiler_repair_description = State()
    boiler_repair_video_or_photo = State()
    boiler_repair_address = State()
    boiler_repair_accept_request = State()

    boiler_rent_type = State()
    boiler_rent_technical_type = State()
    boiler_rent_accept_request = State()

    boiler_technical_catalog_type_choose = State()
    boiler_ask_budget = State()
    boiler_ask_place_format = State()
    boiler_tech_cat_address = State()
    boiler_accept_tech_cat_request = State()

    boiler_barista_training_choose_count = State()
    boiler_barista_training_accept_request = State()

    boiler_send_task_waiting_status = State()
    boiler_upload_file_waiting_status = State()

    boiler_profile_choose = State()
    boiler_profile_choose_for_change = State()
