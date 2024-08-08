import sqlite3

from core.app_logger.logger import Logger

from database.connect import connect_wal_mode
from entities.secret_record import SecretRecord


logger = Logger("db-queries")


def insert_secret(secret_record: SecretRecord) -> int | None:
    query = """
            INSERT INTO secrets_to_share (user_email, secret, hash_link, passphrase_applied,
                                          expiration_time, burned, viewed, creation_datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            return SecretRecord(
                user_email=result[1],
                secret=result[2],
                hash_link=result[3],
                passphrase_applied=result[4],
                expiration_time=result[5],
                burned=result[6],
                viewed=result[7],
                creation_datetime=result[8]
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
