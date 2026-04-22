from typing import Protocol, Self
from jose import jwt
from datetime import datetime, UTC, timedelta
from school_site.settings import settings


MINUTES_TIME = settings.email_service.token_lifetime_minutes
ALGORITHM = settings.email_service.token_algorithm
SECRET_KEY = settings.email_service.secret_key
TRUE_SETTINGS_TOKEN = {
    "iss": "main-service", 
    "permissions": ["send:email"]
}

class InternalTokenServiceProtocol(Protocol):
    def generate_internal_token(self: Self) -> str:
        ...

class InternalTokenService(InternalTokenServiceProtocol):
    def generate_internal_token(self: Self) -> str:
        
        payload = {
            "iss": TRUE_SETTINGS_TOKEN["iss"],
            "permissions": TRUE_SETTINGS_TOKEN["permissions"],
            "exp": datetime.now(UTC) + timedelta(minutes=MINUTES_TIME)
        }
        
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )