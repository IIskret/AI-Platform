from functools import lru_cache
import time
import uuid

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError

from src.core.exceptions import InvalidTokenExc, TokenExpireError
from src.core.jwt_settings import JWTSettings, get_jwt_settings


class JWTService:
    def __init__(self, settings: get_jwt_settings):
        self._settings: JWTSettings = settings

    def _create_token(self, user_id: str, token_type: str, expire_seconds: int) -> str:
        now = int(time.time())
        token_payload = {
            "sub": user_id,
            "type": token_type,
            "iss": self._settings.jwt_iss,
            "aud": self._settings.jwt_aud,
            "iat": now,
            "exp": now + expire_seconds,
            "jti": str(uuid.uuid4())
        }

        return jwt.encode(
            token_payload,
            self._settings.private_key,
            algorithm=self._settings.jwt_algorithm
        )

    def create_access_token(self, user_id) -> str:
        return self._create_token(
            user_id=user_id,
            token_type="access",
            expire_seconds=self._settings.access_token_expire_minutes * 60
        )

    def create_refresh_token(self, user_id) -> str:
        return self._create_token(
            user_id=user_id,
            token_type="refresh",
            expire_seconds=self._settings.refresh_token_expire_days * 86400
        )

    def verify_token(self, token: str, expected_type: str) -> dict:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self._settings.public_key,
                algorithms=[self._settings.jwt_algorithm],
                audience=self._settings.jwt_aud,
                issuer=self._settings.jwt_iss,
                options={
                    "require": ['sub', 'type', 'iss', 'aud', 'exp', 'jti', 'iat']
                }
            )

            if payload.get("type") != expected_type:
                raise InvalidTokenError(
                    f"Invalid token type. Expected: {expected_type}"
                )

            return payload
        except ExpiredSignatureError:
            raise TokenExpireError(
                "Token has expired"
            )
        except PyJWTError:
            raise InvalidTokenExc(
                "Invalid token"
            )


