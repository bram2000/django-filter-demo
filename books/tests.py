from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
import json

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, BookListSerializer
from .filters import BookFilter


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="J.K. Rowling",
            email="jk@example.com",
            bio="Famous author of Harry Potter series",
            birth_date=date(1965, 7, 31)
        )

    def test_author_creation(self):
        self.assertEqual(self.author.name, "J.K. Rowling")
        self.assertEqual(self.author.email, "jk@example.com")
        self.assertEqual(self.author.bio, "Famous author of Harry Potter series")
        self.assertEqual(self.author.birth_date, date(1965, 7, 31))

    def test_author_str_representation(self):
        self.assertEqual(str(self.author), "J.K. Rowling")

    def test_author_ordering(self):
        author2 = Author.objects.create(name="A.A. Milne")
        author3 = Author.objects.create(name="Z.Z. Top")
        
        authors = list(Author.objects.all())
        self.assertEqual(authors[0].name, "A.A. Milne")
        self.assertEqual(authors[1].name, "J.K. Rowling")
        self.assertEqual(authors[2].name, "Z.Z. Top")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            isbn="9780747532699",
            publication_date=date(1997, 6, 26),
            price=Decimal("19.99"),
            genre="Fantasy"
        )
        self.book.authors.add(self.author)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Harry Potter and the Philosopher's Stone")
        self.assertEqual(self.book.isbn, "9780747532699")
        self.assertEqual(self.book.publication_date, date(1997, 6, 26))
        self.assertEqual(self.book.price, Decimal("19.99"))
        self.assertEqual(self.book.genre, "Fantasy")
        self.assertIn(self.author, self.book.authors.all())

    def test_book_str_representation(self):
        self.assertEqual(str(self.book), "Harry Potter and the Philosopher's Stone")

    def test_book_ordering(self):
        book2 = Book.objects.create(title="A Book")
        book3 = Book.objects.create(title="Z Book")
        
        books = list(Book.objects.all())
        self.assertEqual(books[0].title, "A Book")
        self.assertEqual(books[1].title, "Harry Potter and the Philosopher's Stone")
        self.assertEqual(books[2].title, "Z Book")


class AuthorSerializerTest(TestCase):
    def setUp(self):
        self.author_data = {
            'name': 'J.K. Rowling',
            'email': 'jk@example.com',
            'bio': 'Famous author',
            'birth_date': '1965-07-31'
        }
        self.author = Author.objects.create(**self.author_data)

    def test_author_serializer_contains_expected_fields(self):
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'email', 'bio', 'birth_date']))

    def test_author_serializer_valid_data(self):
        serializer = AuthorSerializer(data=self.author_data)
        self.assertTrue(serializer.is_valid())

    def test_author_serializer_invalid_email(self):
        invalid_data = self.author_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = AuthorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class BookSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book_data = {
            'title': 'Harry Potter',
            'isbn': '9780747532699',
            'publication_date': '1997-06-26',
            'price': '19.99',
            'genre': 'Fantasy'
        }
        self.book = Book.objects.create(**self.book_data)
        self.book.authors.add(self.author)

    def test_book_serializer_contains_expected_fields(self):
        serializer = BookSerializer(self.book)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'authors', 'isbn', 'publication_date', 'price', 'genre']))

    def test_book_serializer_includes_authors(self):
        serializer = BookSerializer(self.book)
        self.assertEqual(len(serializer.data['authors']), 1)
        self.assertEqual(serializer.data['authors'][0]['name'], 'J.K. Rowling')

    def test_book_list_serializer_authors_as_strings(self):
        serializer = BookListSerializer(self.book)
        self.assertEqual(serializer.data['authors'], ['J.K. Rowling'])


class BookFilterTest(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George R.R. Martin")
        
        self.book1 = Book.objects.create(
            title="Harry Potter",
            genre="Fantasy",
            price=Decimal("19.99")
        )
        self.book1.authors.add(self.author1)
        
        self.book2 = Book.objects.create(
            title="Game of Thrones",
            genre="Fantasy",
            price=Decimal("25.99")
        )
        self.book2.authors.add(self.author2)

    def test_title_filter(self):
        filter_data = {'title': 'Harry'}
        queryset = BookFilter(data=filter_data, queryset=Book.objects.all()).qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.book1)

    def test_genre_filter(self):
        filter_data = {'genre': 'Fantasy'}
        queryset = BookFilter(data=filter_data, queryset=Book.objects.all()).qs
        self.assertEqual(queryset.count(), 2)

    def test_price_range_filter(self):
        filter_data = {'min_price': 20, 'max_price': 30}
        queryset = BookFilter(data=filter_data, queryset=Book.objects.all()).qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.book2)

    def test_authors_filter(self):
        filter_data = {'authors': [self.author1.id]}
        queryset = BookFilter(data=filter_data, queryset=Book.objects.all()).qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.book1)


class TemplateViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter")
        self.book.authors.add(self.author)

    def test_author_list_view(self):
        response = self.client.get(reverse('books:author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/author_list.html')
        self.assertContains(response, 'J.K. Rowling')

    def test_author_detail_view(self):
        response = self.client.get(reverse('books:author_detail', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/author_detail.html')
        self.assertContains(response, 'J.K. Rowling')

    def test_book_list_view(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertContains(response, 'Harry Potter')

    def test_book_detail_view(self):
        response = self.client.get(reverse('books:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, 'Harry Potter')


class AuthorAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Clear existing data and create fresh test data
        Author.objects.all().delete()
        self.author_data = {
            'name': 'J.K. Rowling',
            'email': 'jk@example.com',
            'bio': 'Famous author',
            'birth_date': '1965-07-31'
        }
        self.author = Author.objects.create(**self.author_data)

    def test_get_authors_list(self):
        url = reverse('books:author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check results count in paginated response
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'J.K. Rowling')

    def test_get_author_detail(self):
        url = reverse('books:author-detail', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')

    def test_create_author(self):
        url = reverse('books:author-list')
        new_author_data = {
            'name': 'George R.R. Martin',
            'email': 'grrm@example.com',
            'bio': 'Game of Thrones author',
            'birth_date': '1948-09-20'
        }
        response = self.client.post(url, new_author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(response.data['name'], 'George R.R. Martin')

    def test_update_author(self):
        url = reverse('books:author-detail', args=[self.author.id])
        updated_data = {'name': 'Joanne Rowling', 'email': 'jk@example.com'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, 'Joanne Rowling')

    def test_delete_author(self):
        url = reverse('books:author-detail', args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_search_authors(self):
        Author.objects.create(name="George R.R. Martin", bio="Fantasy author")
        url = reverse('books:author-list')
        response = self.client.get(url, {'search': 'Rowling'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'J.K. Rowling')

    def test_ordering_authors(self):
        Author.objects.create(name="A.A. Milne")
        Author.objects.create(name="Z.Z. Top")
        url = reverse('books:author-list')
        response = self.client.get(url, {'ordering': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'A.A. Milne')
        self.assertEqual(response.data['results'][-1]['name'], 'Z.Z. Top')


class BookAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Clear existing data and create fresh test data
        Book.objects.all().delete()
        Author.objects.all().delete()
        
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book_data = {
            'title': 'Harry Potter',
            'isbn': '9780747532699',
            'publication_date': '1997-06-26',
            'price': '19.99',
            'genre': 'Fantasy'
        }
        self.book = Book.objects.create(**self.book_data)
        self.book.authors.add(self.author)

    def test_get_books_list(self):
        url = reverse('books:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter')

    def test_get_book_detail(self):
        url = reverse('books:book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')
        self.assertEqual(len(response.data['authors']), 1)

    def test_create_book(self):
        url = reverse('books:book-list')
        new_book_data = {
            'title': 'Game of Thrones',
            'isbn': '9780553103540',
            'publication_date': '1996-08-01',
            'price': '25.99',
            'genre': 'Fantasy'
        }
        response = self.client.post(url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Game of Thrones')

    def test_update_book(self):
        url = reverse('books:book-detail', args=[self.book.id])
        updated_data = {'title': 'Harry Potter and the Philosopher\'s Stone'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Harry Potter and the Philosopher\'s Stone')

    def test_delete_book(self):
        url = reverse('books:book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_title(self):
        Book.objects.create(title="Game of Thrones", genre="Fantasy")
        url = reverse('books:book-list')
        response = self.client.get(url, {'title': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter')

    def test_filter_books_by_genre(self):
        Book.objects.create(title="Game of Thrones", genre="Fantasy")
        url = reverse('books:book-list')
        response = self.client.get(url, {'genre': 'Fantasy'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_filter_books_by_price_range(self):
        Book.objects.create(title="Expensive Book", price=Decimal("50.00"))
        url = reverse('books:book-list')
        response = self.client.get(url, {'min_price': 30, 'max_price': 60})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Expensive Book')

    def test_filter_books_by_authors(self):
        author2 = Author.objects.create(name="George R.R. Martin")
        book2 = Book.objects.create(title="Game of Thrones")
        book2.authors.add(author2)
        
        url = reverse('books:book-list')
        response = self.client.get(url, {'authors': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter')

    def test_search_books(self):
        Book.objects.create(title="Game of Thrones", isbn="9780553103540")
        url = reverse('books:book-list')
        response = self.client.get(url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter')

    def test_ordering_books(self):
        Book.objects.create(title="A Book")
        Book.objects.create(title="Z Book")
        url = reverse('books:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'A Book')
        self.assertEqual(response.data['results'][-1]['title'], 'Z Book')

    def test_by_genre_action(self):
        Book.objects.create(title="Game of Thrones", genre="Fantasy")
        url = reverse('books:book-by-genre')
        response = self.client.get(url, {'genre': 'Fantasy'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_expensive_books_action(self):
        Book.objects.create(title="Expensive Book", price=Decimal("75.00"))
        url = reverse('books:book-expensive-books')
        response = self.client.get(url, {'min_price': 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Expensive Book')

    def test_expensive_books_default_min_price(self):
        Book.objects.create(title="Expensive Book", price=Decimal("75.00"))
        url = reverse('books:book-expensive-books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Expensive Book')


class APIIntegrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(
            title="Harry Potter",
            isbn="9780747532699",
            price=Decimal("19.99"),
            genre="Fantasy"
        )
        self.book.authors.add(self.author)

    def test_full_crud_workflow(self):
        # Create
        author_data = {'name': 'New Author', 'email': 'new@example.com'}
        author_response = self.client.post(reverse('books:author-list'), author_data)
        self.assertEqual(author_response.status_code, status.HTTP_201_CREATED)
        
        # Read
        author_detail = self.client.get(reverse('books:author-detail', args=[author_response.data['id']]))
        self.assertEqual(author_detail.status_code, status.HTTP_200_OK)
        
        # Update
        update_response = self.client.patch(
            reverse('books:author-detail', args=[author_response.data['id']]),
            {'name': 'Updated Author'}
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Delete
        delete_response = self.client.delete(reverse('books:author-detail', args=[author_response.data['id']]))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_book_with_multiple_authors(self):
        author2 = Author.objects.create(name="Co-author")
        book_data = {
            'title': 'Collaborative Book',
            'isbn': '9781234567890',
            'price': '29.99',
            'genre': 'Fiction'
        }
        
        # Create book
        book_response = self.client.post(reverse('books:book-list'), book_data)
        self.assertEqual(book_response.status_code, status.HTTP_201_CREATED)
        
        # Add authors through the API (this would require additional endpoints or manual DB manipulation)
        book = Book.objects.get(id=book_response.data['id'])
        book.authors.add(self.author, author2)
        
        # Verify book has multiple authors
        book_detail = self.client.get(reverse('books:book-detail', args=[book.id]))
        self.assertEqual(len(book_detail.data['authors']), 2)
