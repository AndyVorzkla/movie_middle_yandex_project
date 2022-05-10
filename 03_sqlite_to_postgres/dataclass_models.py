import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class UUID:
    id: uuid.UUID


@dataclass(frozen=True)
class Timestamps:
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Genre(UUID, Timestamps):
    name: str
    description: str


@dataclass(frozen=True)
class Filmwork(UUID, Timestamps):
    title: str
    description: str
    creation_date: datetime.date
    file_path: str
    type: str
    rating: float = field(default=0.0)
    # default_factory для функции без аргументов


@dataclass(frozen=True)
class Person(UUID, Timestamps):
    full_name: str

@dataclass(frozen=True)
class GenreFilmwork(UUID):
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime


@dataclass(frozen=True)
class PersonFilmwork(UUID):
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime
