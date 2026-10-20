from fastapi import APIRouter, Depends, Response, status

from src.app.depends import get_user_service
from src.core.cookies_settings import CookiesSettings, get_cookies_settings
from src.dto.user.auth_result import AuthResult
from src.dto.user.user_auth_schema import UserAuth
from src.services.user_service import UserService

cookies: CookiesSettings = get_cookies_settings()

user_router = APIRouter(
    prefix="/auth",
    tags=["User"]
)

@user_router.post("/registration", status_code=status.HTTP_204_NO_CONTENT)
async def registration(
    schema: UserAuth,
    response: Response,
    user_service: UserService = Depends(get_user_service)
):
    result: AuthResult = await user_service.registration(schema)
    response.set_cookie("access_token", result.access_token, httponly=cookies.httponly, secure=cookies.secure, samesite=cookies.samesite, max_age=cookies.access_token_expire_minutes * 60)
    response.set_cookie("refresh_token", result.refresh_token, httponly=cookies.httponly, secure=cookies.secure, samesite=cookies.samesite, max_age=cookies.access_token_expire_minutes * 86400)



@user_router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login(
    schema: UserAuth,
    response: Response,
    user_service: UserService = Depends(get_user_service)
):
    result = await user_service.login(schema)
    response.set_cookie("access_token", result.access_token, httponly=cookies.httponly, secure=cookies.secure, samesite=cookies.samesite, max_age=cookies.access_token_expire_minutes * 60)
    response.set_cookie("refresh_token", result.refresh_token, httponly=cookies.httponly, secure=cookies.secure, samesite=cookies.samesite, max_age=cookies.refresh_token_expire_days * 86400)


@user_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie(
        "access_token",
        httponly=cookies.httponly,
        secure=cookies.secure,
        samesite=cookies.samesite
    )
    response.delete_cookie(
        "refresh_token",
        httponly=cookies.httponly,
        secure=cookies.secure,
        samesite=cookies.samesite
    )
