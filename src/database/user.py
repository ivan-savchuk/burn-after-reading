from database.connect import connect_wal_mode


def check_for_api_key(api_key: str) -> bool:
    with connect_wal_mode() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM app_users WHERE api_key = ?)",
            (api_key,),
        )
        return cursor.fetchone()[0]
