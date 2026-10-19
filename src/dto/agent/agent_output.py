from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class AgentOutput(BaseModel):
    agent_id: Optional[UUID] = Field(
        default=None
    )
    name: str = Field(
        min_length=1
    )
    description: str = Field(
        min_length=1
    )
    system_prompt: str = Field(
        min_length=1
    )
    model: str = Field(
        min_length=1
    )
    temperature: float = Field(
        gt=0.0,
        le=2.0
    )