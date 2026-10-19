from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.infrastructure.logging.logger import logger


class PasswordHasherService:
    def __init__(self):
        self._ph = PasswordHasher()

    def hashing(self, password: str) -> str:
        return self._ph.hash(password)

    def verify_password(self, db_hash: str, password: str) -> bool:
        try:
            return self._ph.verify(
                hash=db_hash,
                password=password
            )
        except VerifyMismatchError:
            logger.info("invalid password")
            return False
