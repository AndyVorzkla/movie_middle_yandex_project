import sqlite3
import dataclasses
from dataclass_models import Genre, GenreFilmwork, Filmwork, PersonFilmwork, Person


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection, batch_size: int):
        self.conn = connection
        self.curs = connection.cursor()
        self.BATCH_SIZE = batch_size

    def __load_data_from_table_generator(self, table_name: str, data_class: dataclasses.dataclass):
        """ Создается генератор """
        self.curs.execute(f'SELECT * FROM {table_name};')

        try:
            while True:
                # Выгружаем пачку данных с размером BATCH_SIZE
                data = self.curs.fetchmany(self.BATCH_SIZE)
                # Проход по каждой SqliteRow, создание из нее словаря и создание инстанса dataclass
                batch_data = [data_class(**dict(row)) for row in data]

                if not data:
                    # Выходим из цикла если данных больше нет
                    break

                yield batch_data
        except Exception as _ex:
            print(_ex)

    def load_movies(self) -> dict:
        tables = {
            'film_work': Filmwork,
            'genre': Genre,
            'genre_film_work': GenreFilmwork,
            'person': Person,
            'person_film_work': PersonFilmwork,
        }
        data = {}
        for table, dataclass in tables.items():
            data.update({f'{table}': self.__load_data_from_table_generator(table, dataclass)})

        return data

    # def load_all_data(self):
    #     """
    #     Возвращает список из словарей, в которых ключ - название таблицы, а значения - список со словарями,
    #     каждый словарь - строка данных из этой таблицы
    #     :return: list
    #     """
    #     self.curs.execute('SELECT name FROM sqlite_master where type="table"')
    #     table_names_row = self.curs.fetchall()
    #     table_names = [table['name'] for table in table_names_row]
    #     data = []
    #     for table_name in table_names[0:1]:
    #         table_data = self.load_data_from_table(table_name)
    #         data.append({f'{table_name}': table_data})
    #     return data
