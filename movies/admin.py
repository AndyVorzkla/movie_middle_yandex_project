from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInLine(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInLine(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInLine, PersonFilmworkInLine)  # PersonFilmworkInLine

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')
    # Фильтрация в списке
    list_filter = ('type', 'genres',)
    # Поиск по полям
    search_fields = ('title', 'description', 'id')
    # date_hierarchy = ('creation_date')
