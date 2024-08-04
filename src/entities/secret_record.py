from pydantic import BaseModel, Field

from entities.enums import ExpirationTime


class SecretRecord(BaseModel):
    user_email: str | None = Field(default=None)
    secret: str
    hash_link: str
    passphrase_applied: int = Field(default=0)
    expiration_datetime: ExpirationTime = ExpirationTime.SEVEN_DAYS
    burned: int = Field(default=0)
    viewed: int = Field(default=0)

    def to_tuple(self):
        return tuple(self.model_dump().values())
