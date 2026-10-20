from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.database_settings import get_db_settings
from src.infrastructure.logging.logger import logger


class DataBaseConnect:
    def __init__(self):
        self._database = get_db_settings()
        self._async_engine: AsyncEngine | None = None
        self._async_session: AsyncSession | None = None

    @property
    def create_engine(self) -> AsyncEngine:
        try:
            if self._async_engine is None:
                self._async_engine = create_async_engine(
                    self._database.dsn_asyncpg,
                    pool_size=self._database.pool_size,
                    max_overflow=self._database.max_overflow,
                    pool_timeout=self._database.pool_timeout,
                    pool_pre_ping=True,
                    echo=True
                )
            return self._async_engine
        except SQLAlchemyError as exc:
            logger.error(f"Database not connected, reason: {exc}")
            raise

    def create_session(self) -> async_sessionmaker[AsyncSession]:
        try:
            if self._async_session is None:
                self._async_session = async_sessionmaker(
                    bind=self.create_engine,
                    expire_on_commit=False,
                    class_=AsyncSession
                )
            return self._async_session
        except SQLAlchemyError as exc:
            logger.error(f"Database connection failed, reason: {exc}")
            raise

    async def disconnect(self) -> None:
        await self._async_engine.dispose()
        return
