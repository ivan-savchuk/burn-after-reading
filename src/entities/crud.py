from pydantic import BaseModel

from entities.enums import ExpirationTime


class SecretCreate(BaseModel):
    secret: str
    passphrase: str | None = None
    expiration_time: ExpirationTime = ExpirationTime.SEVEN_DAYS


class SecretDNSLink(BaseModel):
    dns_html_link: str
    dns_api_link: str


class SecretData(BaseModel):
    secret: str


class SecretRequest(BaseModel):
    passphrase: str | None = None
