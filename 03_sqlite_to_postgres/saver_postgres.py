from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
from dataclasses import asdict
from typing import Generator

PAGE_SIZE = 500


class PostgresSaver:
    """ Загрузка данных в PostgreSQL """

    def __init__(self, connection: _connection, batch_size: int):
        self.conn = connection
        self.curs = connection.cursor()
        self.BATCH_SIZE = batch_size

    def save_all_data(self, data: dict):
        for table_name, data_generator in data.items():
            self.__save_data_to_table(table_name, data_generator)

    def __save_data_to_table(self, table_name: str, data_generator: Generator):
        """ Заполнение базы PostgreSQL всех таблиц по очереди с учетом совпадения case """
        try:
            dataclasses_objects = next(data_generator)
            while dataclasses_objects:
                match table_name:
                    case 'film_work':
                        query = 'INSERT INTO content.film_work' \
                                '(id, title, description, creation_date, rating, type,' \
                                ' created, modified, file_path, certificate)' \
                                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' \
                                'ON CONFLICT (id) DO NOTHING;'

                        insert_data = [
                            (film_work.id, film_work.title, film_work.description, film_work.creation_date,
                             film_work.rating, film_work.type, film_work.created_at, film_work.updated_at,
                             film_work.file_path, '')
                            for film_work in dataclasses_objects
                        ]

                        execute_batch(self.curs, query, insert_data, page_size=PAGE_SIZE)
                        self.conn.commit()

                        dataclasses_objects = next(data_generator)

                    case 'genre':
                        query = 'INSERT INTO content.genre' \
                                '(id, name, created, modified, description)' \
                                'VALUES (%s, %s, %s, %s, %s)' \
                                'ON CONFLICT (id) DO NOTHING;'

                        insert_data = [
                            (genre.id, genre.name, genre.created_at,
                             genre.updated_at, genre.description)
                            for genre in dataclasses_objects
                        ]

                        execute_batch(self.curs, query, insert_data, page_size=PAGE_SIZE)
                        self.conn.commit()
                        dataclasses_objects = next(data_generator)

                    case 'person':
                        query = 'INSERT INTO content.person' \
                                '(id, full_name, created, modified)' \
                                'VALUES (%s, %s, %s, %s)' \
                                'ON CONFLICT (id) DO NOTHING;'

                        insert_data = [
                            (person.id, person.full_name, person.created_at,
                             person.updated_at)
                            for person in dataclasses_objects
                        ]

                        execute_batch(self.curs, query, insert_data, page_size=PAGE_SIZE)
                        self.conn.commit()
                        dataclasses_objects = next(data_generator)

                    case 'person_film_work':
                        query = 'INSERT INTO content.person_film_work' \
                                '(id, film_work_id, person_id, role, created)' \
                                'VALUES (%s, %s, %s, %s, %s)' \
                                'ON CONFLICT (id) DO NOTHING;'

                        insert_data = [
                            (person_film_work.id, person_film_work.film_work_id, person_film_work.person_id,
                             person_film_work.role, person_film_work.created_at)
                            for person_film_work in dataclasses_objects
                        ]

                        execute_batch(self.curs, query, insert_data, page_size=PAGE_SIZE)
                        self.conn.commit()
                        dataclasses_objects = next(data_generator)

                    case 'genre_film_work':
                        query = 'INSERT INTO content.genre_film_work' \
                                '(id, film_work_id, genre_id, created)' \
                                'VALUES (%s, %s, %s, %s)' \
                                'ON CONFLICT (id) DO NOTHING;'

                        insert_data = [
                            (genre_film_work.id, genre_film_work.film_work_id, genre_film_work.genre_id,
                             genre_film_work.created_at)
                            for genre_film_work in dataclasses_objects
                        ]

                        execute_batch(self.curs, query, insert_data, page_size=PAGE_SIZE)
                        self.conn.commit()
                        dataclasses_objects = next(data_generator)

        except StopIteration as err:
            print(f'Stop iteration {table_name}')

        # query = f'INSERT INTO {table_name} '
