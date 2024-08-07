import sqlite3

from config.sqlite_config import SQLiteConfig


def connect_wal_mode() -> sqlite3.Connection:
    """
    Connect to a SQLite database with WAL mode enabled.
    :return: A connection object to the database.
    """
    db_config = SQLiteConfig().get_config()

    conn = sqlite3.connect(db_config.get("FILE_PATH"))

    conn.execute(f"PRAGMA journal_mode={db_config.get("JORNAL_MODE")}")
    conn.execute(f"PRAGMA page_size={db_config.get("PAGE_SIZE")}")
    conn.execute(f"PRAGMA cache_size=-{db_config.get("CACHE_SIZE")}")
    conn.execute(f"PRAGMA synchronous={db_config.get("SYNCHRONOUS")}")
    conn.execute(f"PRAGMA temp_store={db_config.get("TEMP_STORE")}")

    return conn
