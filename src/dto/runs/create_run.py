from pydantic import BaseModel, Field


class CreateRun(BaseModel):
    input: str = Field(
        min_length=1
    )