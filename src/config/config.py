import os
from abc import abstractmethod


class Config:

    def get_config(self) -> dict:
        config = self.read_from_env()
        self.validate_config(config)
        return config

    @abstractmethod
    def read_from_env(self) -> dict:
        pass

    @staticmethod
    def validate_config(config: dict) -> None:
        missing_data = []
        for key, value in config.items():
            if not value:
                missing_data.append(f"\n- '{key}' is required to be set as environment variable;")

        if missing_data:
            raise ValueError("Missing variables to be set:" + "".join(missing_data))


class AppConfig(Config):

    def read_from_env(self) -> dict:
        return {
            "PORT": os.getenv("PORT"),
            "HOST": os.getenv("HOST"),
            "DEFAULT_PASSPHRASE": os.getenv("DEFAULT_PASSPHRASE")
        }
