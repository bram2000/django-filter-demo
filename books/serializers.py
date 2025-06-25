from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'birth_date']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'isbn', 'publication_date', 'price', 'genre']


class BookListSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'isbn', 'publication_date', 'price', 'genre'] 