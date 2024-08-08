from datetime import datetime

from fastapi import HTTPException

from core.config.config import AppConfig

from entities.secret_record import SecretRecord


cfg = AppConfig().get_config()


class Checker:

    @staticmethod
    def _raise_if_viewed(secret: SecretRecord) -> None:
        if secret.viewed:
            raise HTTPException(status_code=404, detail={"msg": "Secret not found"})

    @staticmethod
    def _raise_if_burned(secret: SecretRecord) -> None:
        if secret.burned:
            raise HTTPException(status_code=404, detail={"msg": "Secret has been burned"})

    @staticmethod
    def _raise_if_expired(secret: SecretRecord) -> None:
        if secret.get_expiration_datetime() < datetime.now():
            raise HTTPException(status_code=404, detail={"msg": "Secret has expired"})

    @classmethod
    def apply_checks(cls, secret: SecretRecord) -> None:
        cls._raise_if_viewed(secret)
        cls._raise_if_burned(secret)
        cls._raise_if_expired(secret)
