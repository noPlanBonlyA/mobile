from pydantic import BaseModel, EmailStr
from .enums import EmailStatus
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from notification_email_service.core.schemas import CreateBaseModel, UpdateBaseModel
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class EmailBase(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    
class EmailCreate(CreateBaseModel, EmailBase):
    pass

class EmailLogBaseDB(EmailBase):
    status: EmailStatus
    error: Optional[str] = None
    sent_at: Optional[datetime] = None

class EmailLogCreateDB(CreateBaseModel, EmailLogBaseDB):
    pass

class EmailLogUpdateDB(UpdateBaseModel, EmailLogBaseDB):
    pass

class EmailLogReadDB(EmailLogBaseDB):
    id: UUID
    created_at: datetime

class TokenDataReadSchema(BaseModel):
    iss: str
    permissions: List[str]
    exp: datetime