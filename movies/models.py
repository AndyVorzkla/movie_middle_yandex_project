import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.validators import validate_0_100_rating


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add автоматически выставит дату создания записи
    modified = models.DateTimeField(auto_now=True)  # auto_now изменится при каждом обновлении записи

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Явно объявляем id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('genre_name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = '"content"."genre"'  # or "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
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
        # managed = False
        db_table = "content\".\"person"
        verbose_name = _('actor')
        verbose_name_plural = _('actors')


class Filmwork(UUIDMixin, TimeStampedMixin):
    # class Type(models.TextChoices):
    #     MOVIE = 'movie'
    #     TV_SHOW = 'tv_show'

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
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        # сообщает джанго что не нужно создавать таблицу по этой миграции, связывает с существующей
        # и не нужно отслеживать изменения
        # managed = False
        # ordering = ['-creation_date']
        db_table = "content\".\"film_work"
        verbose_name = _('film_production')
        verbose_name_plural = _('film_productions')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # managed = False
        db_table = "content\".\"person_film_work"
