from fastapi import Response
from school_site.settings import settings


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # TODO: с HTTPS в проде
        samesite="lax",
        expires=settings.access_token.token_lifetime_minutes * 60,
        path="/"
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # TODO: с HTTPS в проде
        samesite="lax",
        expires=settings.refresh_token.token_lifetime_days * 24 * 60 * 60,
        path="/"
    )