from dataclasses import dataclass
from datetime import datetime

TECHNICAL_PROBLEM_KEY = "technical_problem"

rent_keys = {
    "daily": 'суточная',
    "monthly": "помесячно"
}


@dataclass
class TechnicalProblemDialog:
    id: int
    name: str
