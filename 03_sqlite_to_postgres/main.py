import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from dotenv import load_dotenv
from loader_sqlite import SQLiteLoader
from saver_postgres import PostgresSaver

load_dotenv()

# размер пачки
BATCH_SIZE = 200


@contextmanager
def open_sqlite_db(db_path: str):
    """ Контекстный менеджер для SQLITE """
    conn = sqlite3.connect(db_path)
    # По-умолчанию SQLite возвращает строки в виде кортежа значений. Эта строка указывает, что данные должны быть в формате "ключ-значение"
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def open_postgres_db(config: dict):
    """ Контекстный менеджер для PostgreSQL """
    # Стандартный контекстный менеджер не закрывает соединения при выходе из блока with, а только закрывает транзакцию
    # делает коммит, если не вышло исключения
    conn = psycopg2.connect(**config, cursor_factory=DictCursor)
    try:
        yield conn
    finally:
        conn.close()


class DataConn:

    def __int__(self, db_path: str):
        pass


def load_from_sqlite(sqlite_conn: sqlite3.Connection) -> dict:
    """ Основной метод загрузки данных из SQLite """
    sqlite_loader = SQLiteLoader(sqlite_conn, BATCH_SIZE)
    data = sqlite_loader.load_movies()
    return data


def load_to_postgresql(psql_conn: psycopg2.extensions.connection, data: dict):
    """ Основоной метод загрузки данных в PostgreSQL """
    postgres_saver = PostgresSaver(psql_conn, BATCH_SIZE)
    postgres_saver.save_all_data(data)


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
    with open_sqlite_db(sqlite_db_path) as sqlite_conn, open_postgres_db(dsn) as psql_conn:
        data_sqlite = load_from_sqlite(sqlite_conn)
        load_to_postgresql(psql_conn, data_sqlite)

        # with conn_connect(sqlite_db_path) as sqlite_conn, psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn:
    #     load_from_sqlite(sqlite_conn, pg_conn)
