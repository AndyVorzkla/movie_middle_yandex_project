import random
import uuid
import psycopg2

from datetime import datetime
from faker import Faker
from psycopg2.extras import execute_batch

fake = Faker()

dsn = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}
# search_path=content, не нужно писать INSERT INTO content(!).person
PERSON_COUNT = 100000
PAGE_SIZE = 5000

now = datetime.utcnow()
# connect подсоединяет к базе данных
# cursor содержит методы для работы с sql запросами

with psycopg2.connect(**dsn) as connection, connection.cursor() as cursor:
    # connection.autocommit = True не нужно вызывать commit
    # Проверка успешного подключения к базе
    cursor.execute(
        "SELECT version();"
    )
    #возвращает кортеж либо None
    print(f"server version: {cursor.fetchone()}")

    # Заполнение таблицы Person

    # person_ids = [str(uuid.uuid4()) for _ in range(PERSON_COUNT)]
    # query = 'INSERT INTO person (id, full_name, created, modified) VALUES (%s, %s, %s, %s)'
    # data = [(pk, fake.last_name(), now, now) for pk in person_ids]
    # execute_batch(cursor, query, data, page_size=PAGE_SIZE)
    # connection.commit() Не нужно, так как execute_batch делает коммит
    #
    # Заполнение таблицы PersonFilmWork
    # person_film_work_data = []
    # roles = ['actor', 'producer', 'director']

    # Получаю id всех людей в person
    # cursor.execute('SELECT id FROM person')
    # person_ids = [data[0] for data in cursor.fetchall()]

    # fetchall() создается список из кортежей c одним элементом - id фильма, заполненный через CREATE EXTENSION...
    # cursor.execute('SELECT id FROM film_work')
    # film_works_ids = [data[0] for data in cursor.fetchall()]

    # for film_work_id in film_works_ids:
    #     for person_id in random.sample(person_ids, 5):
    #         role = random.choice(roles)
    #         person_film_work_data.append((str(uuid.uuid4()), film_work_id, person_id, role, now))
    #
    # query = 'INSERT INTO person_film_work (id, film_work_id, person_id, role, created) VALUES (%s, %s, %s, %s, %s)'
    # execute_batch(cursor, query, person_film_work_data, page_size=PAGE_SIZE)
    # connection.commit()