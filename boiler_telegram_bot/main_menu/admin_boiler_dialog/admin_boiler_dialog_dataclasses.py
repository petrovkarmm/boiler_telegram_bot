from dataclasses import dataclass
from datetime import datetime

FEEDBACK_KEY = "feedback"


@dataclass
class Feedback:
    id: int
    feedback_text: str
