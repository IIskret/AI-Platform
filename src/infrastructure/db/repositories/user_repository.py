from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UserAlreadyExists
from src.infrastructure.db.models.user_schema import User
from src.infrastructure.logging.logger import logger


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create_user(
        self,
        email: EmailStr,
        password: str
    ) -> User:
        user = User(
            email=email,
            password_hash=password
        )
        self._session.add(user)

        try:
            await self._session.flush()
            return user
        except IntegrityError as e:
            logger.warning(
                f"failed to create user: user already exists, {e}"
            )
            raise UserAlreadyExists(
                f"user with email {email} already exist"
            ) from e

    async def select_user(
        self,
        email: EmailStr
    ) -> User | None:
        user = select(User).where(
            User.email==email
        )
        result = await self._session.scalar(user)
        return result
