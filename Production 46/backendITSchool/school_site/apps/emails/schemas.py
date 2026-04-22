from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EmailBase(BaseModel):
    to_email: str
    subject: str
    body: str


class EmailRequestDTO(EmailBase):
    pass    


class EmailResponseDTO(EmailBase):
    id: UUID
    status: str
    error: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime