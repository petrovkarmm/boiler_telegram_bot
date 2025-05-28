from dataclasses import dataclass

TECHNICAL_PROBLEM_KEY = "technical_problem"
PROFILE_KEY = "profile"

TECHNICAL_CATALOG = {
    "horn": 'рожковая',
    "auto": "автоматическая"
}

RENT_TYPE = {
    "daily": "посуточно",
    "monthly": "помесячно",
}


@dataclass
class TechnicalProblemDialog:
    id: int
    name: str


@dataclass
class ProfileDialog:
    id: int
    name: str

    @staticmethod
    def formatted_name(name: str, firm_type):
        if firm_type == 'individual':
            return f'Физ. лицо "{name}"'
        return name
