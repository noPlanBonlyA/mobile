from typing import Protocol, Self
from jose import jwt, JWTError
import logging
from ..schemas import TokenDataReadSchema
from notification_email_service.settings import settings
from notification_email_service.core.utils.exceptions import PermissionDeniedError

logger = logging.getLogger(__name__)


TRUE_SETTINGS_TOKEN = {
    "iss": "main-service", 
    "permission": "send:email"
}

class TokenServiceProtocol(Protocol):
    def decode_access_token(self: Self, token: str) -> TokenDataReadSchema:
        ...

class TokenService(TokenServiceProtocol):
     def __init__(self: Self) -> None:
         super().__init__()
        
     def decode_access_token(self: Self, token: str) -> TokenDataReadSchema:
        logger.info("Starting token validation")
        try:
            logger.debug("Decoding JWT token")
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt.token_algorithm])
            
            iss = payload.get("iss")
            permissions = payload.get("permissions", [])
            exp = payload.get("exp")
            
            logger.info(f"Token decoded successfully. Issuer: {iss}, Permissions: {permissions}")

            if iss != TRUE_SETTINGS_TOKEN["iss"]:
                logger.warning(f"Invalid issuer. Expected: {TRUE_SETTINGS_TOKEN['iss']}, Got: {iss}")
                raise PermissionDeniedError()
                
            if TRUE_SETTINGS_TOKEN["permission"] not in permissions:
                logger.warning(f"Missing required permission. Required: {TRUE_SETTINGS_TOKEN['permission']}, Got: {permissions}")
                raise PermissionDeniedError()

            logger.info("Token validation successful")
            return TokenDataReadSchema(
                iss=iss,
                permissions=permissions,
                exp=exp
            )
        except JWTError as e:
            logger.error(f"JWT decode error: {str(e)}", exc_info=True)
            raise PermissionDeniedError()
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {str(e)}", exc_info=True)
            raise PermissionDeniedError()