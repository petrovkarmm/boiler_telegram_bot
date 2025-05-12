from dataclasses import dataclass
from datetime import datetime

ADMIN_FEEDBACK_KEY = "feedback"
ADMIN_TECHNICAL_PROBLEM_KEY = "technical_problem"


@dataclass
class AdminFeedbackDialog:
    id: int
    feedback_text: str

    @staticmethod
    def formatted_feedback_text(feedback_text: str):
        return f'{feedback_text[:15]}...'


@dataclass
class AdminTechnicalProblemDialog:
    id: int
    name: str

    @staticmethod
    def formatted_hidden_problems(name: str, hidden: int):
        if hidden == 1:
            return f'🔓 {name} 🔓'
        else:
            return f'{name}'
