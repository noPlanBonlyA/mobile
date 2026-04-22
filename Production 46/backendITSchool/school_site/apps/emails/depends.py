from fastapi import Depends
from .services.auth import InternalTokenServiceProtocol, InternalTokenService
from .clients.emails import EmailClientProtocol, EmailClient

def get_internal_token_service() -> InternalTokenServiceProtocol:
    return InternalTokenService()

def get_email_client(
    token_service: InternalTokenServiceProtocol = Depends(get_internal_token_service)
) -> EmailClientProtocol:
    return EmailClient(token_service)