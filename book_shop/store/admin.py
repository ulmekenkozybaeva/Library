from django.contrib import admin
from .models import Genre, DetailedBook

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(DetailedBook)
class DetailedBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'genre',  'url',)
    list_editable = ('url',)
    list_filter = ('genre',)
    search_fields = ('name', 'author')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('publication_year', 'updated')
