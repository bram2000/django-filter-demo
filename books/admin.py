from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'birth_date']
    search_fields = ['name', 'email']
    list_filter = ['birth_date']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'publication_date', 'price', 'genre']
    list_filter = ['author', 'genre', 'publication_date']
    search_fields = ['title', 'author__name', 'isbn']
    date_hierarchy = 'publication_date'
