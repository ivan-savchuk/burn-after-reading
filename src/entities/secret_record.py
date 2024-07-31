from pydantic import BaseModel, Field


class SecretRecord(BaseModel):
    user_email: str = Field(default=None)
    secret: str
    hash_link: str
    passphrase_applied: int = Field(default=0)
    expiration_datetime: str = Field(default="7d")
    is_burned: int = Field(default=0)
    viewed: int = Field(default=0)

    def to_tuple(self):
        return tuple(self.model_dump().values())