from typing import Protocol
import httpx
from ..schemas import EmailRequestDTO, EmailResponseDTO
from ..services.auth import InternalTokenServiceProtocol
from ..exceptions import EmailServerError
from school_site.settings import settings

class EmailClientProtocol(Protocol):
    async def send_email(self, email_dto: EmailRequestDTO) -> EmailResponseDTO:
        ...


class EmailClient(EmailClientProtocol):
    def __init__(self, token_service: InternalTokenServiceProtocol):
        self.token_service = token_service
        
        
    async def send_email(self, email_dto: EmailRequestDTO) -> EmailResponseDTO:
        token = self.token_service.generate_internal_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                str(settings.email_service.url),
                json=email_dto.model_dump(),
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
            
            if response.status_code != 200:
                raise EmailServerError(
                    status_code=response.status_code,
                    detail=f"Email sending error: {response.text}"
                )
            
            return EmailResponseDTO.model_validate(response.json())