from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.infrastructure.db.models.run_schema import RunStatus


class RunOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    run_id: UUID
    agent_id: UUID
    status: RunStatus
    
    input: str = Field(
        min_length=1
    )
    output: str | None = Field(
        default=None
    )
    error: str | None = Field(
        default=None
    )
    model: str = Field(
        min_length=1
    )
    prompt_version: str = Field(
        min_length=1
    )
    tools_version: str = Field(
        min_length=1
    )
    input_tokens: int | None = Field(
        default=None
    )
    output_tokens: int | None = Field(
        default=None
    )
    latency_ms: int | None = Field(
        default=None
    )
