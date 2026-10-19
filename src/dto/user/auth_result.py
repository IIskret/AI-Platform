from pydantic import BaseModel, Field, ConfigDict

from src.infrastructure.db.models.user_schema import User

class AuthResult(BaseModel):
    model_config=ConfigDict(arbitrary_types_allowed=True)

    user: User
    access_token: str = Field(
        min_length=1
    )
    refresh_token: str = Field(
        min_length=1
    )