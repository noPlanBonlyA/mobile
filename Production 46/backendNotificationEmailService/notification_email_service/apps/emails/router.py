from fastapi import APIRouter, Depends
from .schemas import EmailCreate, EmailLogReadDB, oauth2_scheme
from .use_cases.send_and_save_email import SendAndSaveEmailUseCaseProtocol
from .depends import get_send_and_save_email_use_case

router = APIRouter(prefix='/api/emails', tags=['Emails'])


@router.post("/send/", response_model=EmailLogReadDB)
async def create_student(
    email: EmailCreate,
    token: str = Depends(oauth2_scheme),
    send: SendAndSaveEmailUseCaseProtocol = Depends(get_send_and_save_email_use_case)
):
    return await send(token, email)