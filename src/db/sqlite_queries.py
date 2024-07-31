import sqlite3

from app_logger.logger import Logger
from entities.secret_record import SecretRecord
from config.sqlite_config import SQLiteConfig


logger = Logger("db-queries")


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


def insert_secret(secret_record: SecretRecord) -> int | None:
    query = """
            INSERT INTO secrets_to_share (user_email, secret, hash_link, passphrase_applied,
                                          expiration_datetime, burned, viewed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        with connect_wal_mode() as conn:
            cursor = conn.cursor()
            cursor.execute(query, secret_record.to_tuple())
            return cursor.lastrowid
    except sqlite3.Error as exc:
        logger.error(f"An error occurred: {exc}")
        return None


def get_secret_by_link(hash_link: str) -> SecretRecord | None:
    query = """
        SELECT *
        FROM secrets_to_share
        WHERE hash_link = ?
    """
    try:
        with connect_wal_mode() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (hash_link,))
            result = cursor.fetchone()
            print(result)
            return SecretRecord(
                user_email=result[1],
                secret=result[2],
                hash_link=result[3],
                passphrase_applied=result[4],
                expiration_datetime=result[5],
                burned=result[6],
                viewed=result[7]
            )
    except sqlite3.Error as exc:
        logger.error(f"An error occurred: {exc}")
        return None


def update_viewed_status(hash_link: str, viewed: int) -> None:
    query = """
        UPDATE secrets_to_share
        SET viewed = ?
        WHERE hash_link = ?
    """
    try:
        with connect_wal_mode() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (viewed, hash_link))
    except sqlite3.Error as exc:
        logger.error(f"An error occurred: {exc}")
