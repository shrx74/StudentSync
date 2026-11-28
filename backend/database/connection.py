import os
from dotenv import load_dotenv
from psycopg.conninfo import make_conninfo
from psycopg_pool import ConnectionPool

load_dotenv()


def connection_string():
    url = os.getenv("DATABASE_URL")

    if url:
        return url

    return make_conninfo(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# Reuse open connections instead of connecting for every query
pool = ConnectionPool(
    connection_string(),
    min_size=1,
    max_size=5,
    check=ConnectionPool.check_connection,
    open=False,
)


class Database:

    @staticmethod
    def connect():
        if pool.closed:
            pool.open()

        return pool.connection()
