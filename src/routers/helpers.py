from fastapi import HTTPException

from entities.secret_record import SecretRecord


def raise_if_viewed(secret: SecretRecord) -> None:
    if secret.viewed:
        raise HTTPException(status_code=404, detail={"message": "Secret not found"})
