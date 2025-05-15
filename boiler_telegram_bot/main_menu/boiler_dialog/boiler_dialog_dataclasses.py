from dataclasses import dataclass
from datetime import datetime

TECHNICAL_PROBLEM_KEY = "technical_problem"

TECHNICAL_CATALOG = {
    "horn": 'рожковая',
    "auto": "автоматическая"
}


@dataclass
class TechnicalProblemDialog:
    id: int
    name: str
