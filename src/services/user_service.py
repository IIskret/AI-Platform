from fastapi import HTTPException, status

from src.dto.user.auth_result import AuthResult
from src.dto.user.user_auth_schema import UserAuth
from src.infrastructure.db.models.user_schema import User
from src.infrastructure.db.repositories.user_repository import UserRepository
from src.services.auth.jwt import JWTService
from src.services.auth.password import PasswordHasherService


class UserService:
    def __init__(
        self, 
        user_repository: UserRepository, 
        jwt_service: JWTService
    ) -> None:
        self._user_repository: UserRepository = user_repository
        self._password_hasher_service: PasswordHasherService = PasswordHasherService()
        self._jwt_serivce: JWTService = jwt_service


    async def registration(self, schema: UserAuth) -> AuthResult:
        get_user = await self._user_repository.select_user(
            email=schema.email
        )

        if get_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user with this email already exists"
            )

        hashed_password = self._password_hasher_service.hashing(schema.password)

        user: User = await self._user_repository.create_user(
            email=schema.email,
            password=hashed_password
        )

        return AuthResult(
            user=user,
            access_token=self._jwt_serivce.create_access_token(str(user.id)),
            refresh_token=self._jwt_serivce.create_refresh_token(str(user.id))
        )

    async def login(self, schema: UserAuth) -> AuthResult | None :
        user = await self._user_repository.select_user(
            email=schema.email
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        verify_password = self._password_hasher_service.verify_password(
            db_hash=user.password_hash,
            password=schema.password
        )

        if not verify_password:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Invalid email or password"
            )

        return AuthResult(
            user=user,
            access_token=self._jwt_serivce.create_access_token(str(user.id)),
            refresh_token=self._jwt_serivce.create_refresh_token(str(user.id))
        )

    async def refresh():
        pass
