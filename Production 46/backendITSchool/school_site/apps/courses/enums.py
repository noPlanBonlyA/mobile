from enum import Enum

class AgeCategory(str, Enum):
    ALL_AGES = "All"
    FIVE_TO_EIGHT = "5-8"
    NINE_TO_ELEVEN = "9-11"
    TWELVE_TO_FIFTEEN = "12-15"