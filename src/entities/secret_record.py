from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from entities.enums import ExpirationTime


class SecretRecord(BaseModel):
    user_email: str | None = Field(default=None)
    secret: str
    hash_link: str
    passphrase_applied: int = Field(default=0)
    expiration_time: ExpirationTime = Field(default=ExpirationTime.SEVEN_DAYS)
    burned: int = Field(default=0)
    viewed: int = Field(default=0)
    creation_datetime: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_tuple(self):
        return tuple(self.model_dump().values())

    @staticmethod
    def get_timedelta(value: int, unit: str) -> timedelta:
        match unit:
            case 'm':
                return timedelta(minutes=value)
            case 'h':
                return timedelta(hours=value)
            case _:
                return timedelta(days=value)

    def get_expiration_datetime(self) -> datetime:
        value = int(self.expiration_time[:-1])
        unit = self.expiration_time[-1]

        return datetime.strptime(self.creation_datetime, "%Y-%m-%d %H:%M:%S") + self.get_timedelta(value, unit)
