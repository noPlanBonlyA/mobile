from enum import Enum

class Reason(str, Enum):
    HOMEWORK = "Homework"
    VISIT = "Visit"
    BONUS = "Bonus"
    PENALTY = "Penalty"
    BUY = "Buy"
    OTHER = "Other"