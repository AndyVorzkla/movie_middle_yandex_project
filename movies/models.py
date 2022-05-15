import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.validators import validate_0_100_rating


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('genre_name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = '"content"."genre"'  # or "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    class Gender(models.TextChoices):
        MALE = 'male', _('male'),
        FEMALE = 'female', _('female'),

    full_name = models.TextField(_('fullname'))
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('actor')
        verbose_name_plural = _('actors')


class Filmwork(UUIDMixin, TimeStampedMixin):
    TYPE_CHOICES = [
        ('movie', _('movie')),
        ('tv_show', _('tv_show')),
    ]

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[validate_0_100_rating])
    # choices ожидает [(a,b), (a,b)] , где а фактическое значение, которое будет установлено в модели,
    # а b - удобное для чтение человеком
    type = models.TextField(_('type'), choices=TYPE_CHOICES)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork', related_name='filmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork', related_name='filmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_production')
        verbose_name_plural = _('film_productions')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre_constraint')
        ]


class PersonFilmwork(UUIDMixin):

    class RoleChoices(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        DIRECTOR = 'director', _('Writer')
        WRITER = 'writer', _('Director')
        COMPOSER = 'composer', _('Composer')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=RoleChoices.choices, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            models.Index(fields=['film_work', 'person'], name='film_work_person_idx')
        ]