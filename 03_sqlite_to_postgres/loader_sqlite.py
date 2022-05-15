import logging_setting
import sqlite3
import dataclasses
from dataclass_models import Genre, GenreFilmwork, Filmwork, PersonFilmwork, Person

logger = logging_setting.base_logger

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
                    break

                yield batch_data
        except Exception as _ex:
            logger.error('Ошибка при загрузке данных')

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

        # Проверил логи и в data не окажутся все записи из sqlite
        # В data по ключу будет генератор, который потом через метод next()
        # будет пачками через fetchmany(self.BATCH_SIZE = 200) забирать данные и присваивать
        # переменной dataclasses_objects в методе __save_data_to_table
        # логи в файле sqlite_to_psql_migrate
        return data
