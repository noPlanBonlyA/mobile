from enum import Enum

class EmailStatus(Enum):
    QUEUED = 'queued'
    SENT = 'sent'
    FAILED = 'failed'
