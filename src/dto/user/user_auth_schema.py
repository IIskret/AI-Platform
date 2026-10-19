import string

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError


class UserAuth(BaseModel):
    email: EmailStr = Field(
        min_length=1
    )
    password: str = Field(
        min_length=8
    )

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, v: str) -> str:
        special_characters = set(string.punctuation)

        if not any(i.islower() for i in v):
            raise PydanticCustomError(
                "password_no_lower_case_value",
                "The password must contain lowercase letters",
            )

        if not any(i.isupper() for i in v):
            raise PydanticCustomError(
                "password_no_upper_case_value",
                "The password must contain uppercase letters",
            )

        if not any(i.isdigit() for i in v):
            raise PydanticCustomError(
                "password_no_digit_value",
                "The password must contain digit",
            )

        if not any(char in special_characters for char in v):
            raise PydanticCustomError(
                "password_no_special_char",
                "The password must contain special char (for example: !, @, #, $, %)"
            )

        return v


