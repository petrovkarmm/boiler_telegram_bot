from dataclasses import dataclass
from datetime import datetime

TECHNICAL_PROBLEM_KEY = "technical_problem"

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
