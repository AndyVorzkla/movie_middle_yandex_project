import sqlite3
import uuid
from dataclasses import dataclass, field
from psycopg2.extensions import connection as _connection


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.curs = connection.cursor()

    def load_data_from_table(self, table_name: str):
        self.curs.execute(f'SELECT * FROM {table_name}')
        table_rows = self.curs.fetchall()
        data = [dict(row) for row in table_rows]
        return data

    def load_all_data(self):
        """
        Возвращает список из словарей, в которых ключ - название таблицы, а значения - список со словарями,
        каждый словарь - строка данных из этой таблицы
        :return: list
        """
        self.curs.execute('SELECT name FROM sqlite_master where type="table"')
        table_names_row = self.curs.fetchall()
        table_names = [table['name'] for table in table_names_row]
        data = []
        for table_name in table_names[0:1]:
            table_data = self.load_data_from_table(table_name)
            data.append({f'{table_name}': table_data})
        return data