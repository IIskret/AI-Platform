from collections.abc import AsyncGenerator

from fastapi import Cookie, Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import PyJWTError

from src.core.jwt_settings import get_jwt_settings
from src.infrastructure.db.repositories.user_repository import UserRepository
from src.infrastructure.db.session import DataBaseConnect
from src.services.agent_service import AgentService
from src.services.auth.jwt import JWTService, get_jwt_settings
from src.services.user_service import UserService
from src.infrastructure.db.repositories.agent_repository import AgentRepository
from src.infrastructure.db.repositories.runs_repository import RunsRepository
from src.infrastructure.llm.mistral import MistralProvider
from src.core.llm_api_settings import LLMApiSettings, get_llm_settings
from src.services.runs_service import RunsService


async def get_db() -> DataBaseConnect:
    return DataBaseConnect()


async def get_session(
    request: Request
) -> AsyncGenerator[AsyncSession, None]:

    factory = request.app.state.session_factory
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_agent_repository(session: AsyncSession = Depends(get_session)) -> AgentRepository:
    return AgentRepository(session)

def get_jwt_serivce(jwt: JWTService = Depends(get_jwt_settings)) -> JWTService:
    return JWTService(jwt)

def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    jwt_service: JWTService = Depends(get_jwt_serivce)
) -> UserService:
    return UserService(
        user_repository,
        jwt_service
        )


def get_current_user(
    access_token: str | None = Cookie(None, alias="access_token"),
    jwt_service: JWTService = Depends(get_jwt_serivce)
) -> str:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

    try:
        payload = jwt_service.verify_token(token=access_token, expected_type="access")
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError()
        return user_id
    except (ValueError, PyJWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )


def get_agent_service(
    agent_repository: AgentRepository = Depends(get_agent_repository),
    user_id: str = Depends(get_current_user)
) -> AgentService:
    return AgentService(
        agent_repository,
        user_id
    )


def get_llm_provider(
    llm_settings: LLMApiSettings = Depends(get_llm_settings)
) -> MistralProvider:
    return MistralProvider(
        api_key=llm_settings.mistral_api.get_secret_value()
    )


def get_runs_repository(
    session: AsyncSession = Depends(get_session)
) -> RunsRepository:
    return RunsRepository(session)


def get_runs_service(
    runs_repository: RunsRepository = Depends(get_runs_repository),
    agent_repository: AgentRepository = Depends(get_agent_repository),
    llm_provider: MistralProvider = Depends(get_llm_provider),
    user_id: str = Depends(get_current_user)
) -> RunsService:
    return RunsService(
        runs_repository,
        agent_repository,
        llm_provider,
        user_id
    )