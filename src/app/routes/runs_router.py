from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.app.depends import get_runs_service
from src.dto.runs.run_output import RunOutput
from src.services.runs_service import RunsService

runs_router: APIRouter = APIRouter(
    prefix="/runs",
    tags=["Run"]
)


@runs_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_run(
    id: UUID,
    runs_service: RunsService = Depends(get_runs_service)
) -> RunOutput:
    return await runs_service.get_run(run_id=id)
