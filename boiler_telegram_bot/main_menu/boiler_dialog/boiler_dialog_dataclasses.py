from dataclasses import dataclass
from datetime import datetime

TECHNICAL_PROBLEM_KEY = "technical_problem"


@dataclass
class TechnicalProblemDialog:
    id: int
    name: str
