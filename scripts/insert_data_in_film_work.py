import random
import uuid
from math import floor

import psycopg2
import datetime
from faker import Faker
import random
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
PAGE_SIZE = 5000

now = datetime.datetime.utcnow()

# connect подсоединяет к базе данных
# cursor содержит методы для работы с sql запросами

with psycopg2.connect(**dsn) as connection, connection.cursor() as cursor:
    creation_data = []
    type_data = []
    cursor.execute('SELECT film_work_id FROM person_film_work')
    film_work_id = set([data[0] for data in cursor.fetchall()])
    creation_date = datetime.datetime(1900, 1, 1, 0, 0, 0)
    while creation_date <= datetime.datetime(2021, 1, 1, 0, 0, 0):
        type_data.append('tv_show') if random.random() < 0.3 else type_data.append('movie')

        print(creation_date)
        creation_data.append(creation_date)
        creation_date += datetime.timedelta(hours=1)

    data = [(pk, 'some_name', type_media, creation_date, floor(random.random() * 100), now, now) for pk, creation_date, type_media in zip(film_work_id, creation_data, type_data)]
    query = 'INSERT INTO content.film_work (id, title, type, creation_date, rating, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    execute_batch(cursor, query, data, page_size=PAGE_SIZE)

    # cursor.execute("INSERT INTO content.film_work (id, title, type, creation_date, rating) SELECT uuid_generate_v4(), 'some name', case when RANDOM() < 0.3 THEN 'movie' ELSE 'tv_show' END , date::DATE, floor(random() * 100)")
    # query = 'INSERT INTO content.film_work (id, title, type, creation_date, rating)'
    # query = 'INSERT INTO film_work (id, title, description, creation_date, rating, type, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    # data = [(pk, 'some_name', '',) for pk in film_work_id]
