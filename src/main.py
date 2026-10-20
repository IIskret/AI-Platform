from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.routes.agent_router import agent_router
from src.app.routes.runs_router import runs_router
from src.app.routes.user_router import user_router
from src.infrastructure.db.session import DataBaseConnect
from src.infrastructure.logging.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DataBaseConnect()
    session_factory = db.create_session()

    app.state.db = db
    app.state.session_factory = session_factory
    logger.info("server is running")

    yield

    await db.disconnect()
    logger.info("server stopped")


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(agent_router)
app.include_router(runs_router)


