import uuid
from dataclasses import dataclass
from psycopg2.extensions import connection as _connection


@dataclass(frozen=True)
class Genre:
    id : uuid.UUID = uuid.uuid4()


class PostgresSaver:

    def __init__(self, connection: _connection):
        self.conn = connection
        self.curs = connection.cursor()

    def save_all_data(self, data: list):
        pass
