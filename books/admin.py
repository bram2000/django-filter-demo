from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'birth_date']
    search_fields = ['name', 'email']
    list_filter = ['birth_date']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_authors', 'isbn', 'publication_date', 'price', 'genre']
    list_filter = ['authors', 'genre', 'publication_date']
    search_fields = ['title', 'authors__name', 'isbn']
    date_hierarchy = 'publication_date'
    
    def get_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    get_authors.short_description = 'Authors'
