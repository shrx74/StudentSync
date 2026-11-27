import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


class Database:

    @staticmethod
    def connect():
        url = os.getenv("DATABASE_URL")

        if url:
            return psycopg.connect(url)

        return psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
