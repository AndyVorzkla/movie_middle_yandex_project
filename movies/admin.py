from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork
from django.contrib import admin


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
    inlines = (GenreFilmworkInLine, PersonFilmworkInLine)
    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')
    # Фильтрация в списке
    list_filter = ('type', 'genres',)
    # Поиск по полям
    search_fields = ('title', 'description', 'id')
    # date_hierarchy = ('creation_date')
    prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(
                *self.prefetch_related
            )
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'
