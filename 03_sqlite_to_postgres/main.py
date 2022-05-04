import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from dotenv import load_dotenv
from load_data_sqlite import SQLiteLoader
from record_data_postgres import PostgresSaver
load_dotenv()


@contextmanager
def conn_connect(db_path: str):
    conn = sqlite3.connect(db_path)
    # По-умолчанию SQLite возвращает строки в виде кортежа значений. Эта строка указывает, что данные должны быть в формате "ключ-значение"
    conn.row_factory = sqlite3.Row
    yield conn

    conn.close()

def load_from_sqlite(sql_conn: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_loader = SQLiteLoader(sql_conn)
    data = sqlite_loader.load_all_data()

    postgres_saver = PostgresSaver(pg_conn)
    # postgres_saver.save_all_data(data)

if __name__ == '__main__':
    dsn = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': 'localhost',
        'port': 5432,
        'options': '-c search_path=content',
    }
    sqlite_db_path = os.environ.get('DB_SQLITE_PATH')
    # sqlite_conn = sqlite3.connect(sqlite_db_path)
    with conn_connect(sqlite_db_path) as sqlite_conn, psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)


        # with conn_connect(sqlite_db_path) as sqlite_conn, psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn:
    #     load_from_sqlite(sqlite_conn, pg_conn)

