import os
from config.config import Config


class SQLiteConfig(Config):

    def read_from_env(self) -> dict:
        return {
            "FILE_PATH": os.getenv("FILE_PATH"),
            "JOURNAL_MODE": os.getenv("JOURNAL_MODE"),
            "PAGE_SIZE": os.getenv("PAGE_SIZE"),
            "CACHE_SIZE": os.getenv("CACHE_SIZE"),
            "SYNCHRONOUS": os.getenv("SYNCHRONOUS"),
            "TEMP_STORE": os.getenv("TEMP_STORE")
        }
