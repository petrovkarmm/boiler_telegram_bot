from dataclasses import dataclass
from datetime import datetime

FEEDBACK_KEY = "feedback"


@dataclass
class FeedbackDialog:
    id: int
    feedback_text: str

    @staticmethod
    def formatted_feedback_text(feedback_text: str):
        return f'{feedback_text[:15]}...'
