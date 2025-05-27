from aiogram.fsm.state import StatesGroup, State


class BoilerRegistrationDialog(StatesGroup):
    boiler_registration_user_name = State()
    boiler_registration_itn = State()
    boiler_registration_phone = State()

    boiler_registration_firm_type = State()

    boiler_registration_organization_name = State()

    boiler_registration_accepting = State()
