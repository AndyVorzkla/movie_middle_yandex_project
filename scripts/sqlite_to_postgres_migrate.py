import sqlite3
import psycopg2
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

dsn = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}


@contextmanager
def conn_connect(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn

    conn.close()


def main():
    db_path = os.environ.get('DB_SQLITE_PATH')
    with conn_connect(db_path) as conn_sqlite, \
            psycopg2.connect(**dsn) as conn_postgres, conn_postgres.cursor() as curs_postgres:
        curs_sqlite = conn_sqlite.cursor()

        curs_sqlite.execute("SELECT * FROM film_work;")
        data = curs_sqlite.fetchall()


if __name__ == '__main__':
    main()
