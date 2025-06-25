from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer, BookListSerializer


class AuthorListView(ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    context_object_name = 'author'


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'


# REST API ViewSets
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'birth_date']
    ordering = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'isbn']
    ordering_fields = ['title', 'publication_date', 'price']
    ordering = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        genre = request.query_params.get('genre', '')
        books = self.queryset.filter(genre__icontains=genre)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expensive_books(self, request):
        min_price = request.query_params.get('min_price', 50)
        books = self.queryset.filter(price__gte=min_price)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
