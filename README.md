# Django Filter Demo

A Django project demonstrating the usage of `ModelMultipleChoiceFilter` from the `django-filter` library.

## Overview

This project showcases how to implement and use `ModelMultipleChoiceFilter` for filtering Django model querysets based on multiple choice selections. The demo includes a simple book library system with authors and books, demonstrating various filtering capabilities.

## Features

- **Book Management**: CRUD operations for books with multiple authors
- **Author Management**: CRUD operations for authors
- **Advanced Filtering**: Demonstrates `ModelMultipleChoiceFilter` usage
- **REST API**: Includes serializers for API access
- **Web Interface**: Template-based views for browsing books and authors

## Models

- **Book**: Contains title, publication date, and many-to-many relationship with authors
- **Author**: Contains name and biography fields

## Filtering Examples

The project demonstrates:
- Filtering books by multiple authors
- Filtering by publication date ranges
- Combining multiple filters
- Using `ModelMultipleChoiceFilter` for many-to-many relationships

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run migrations:
   ```bash
   poetry run python manage.py migrate
   ```

3. Create a superuser (optional):
   ```bash
   poetry run python manage.py createsuperuser
   ```

4. Run the development server:
   ```bash
   poetry run python manage.py runserver
   ```

## Usage

- Visit `/books/` to see the book list with filtering options
- Visit `/authors/` to see the author list
- Use the filter forms to test `ModelMultipleChoiceFilter` functionality
- Access the admin interface at `/admin/` for data management

## API Usage

The project includes a REST API with the following endpoints:

### Base URL
All API endpoints are prefixed with `/books/api/`

### Authors API

**List Authors**
```bash
GET /books/api/authors/
```

**Get Author Details**
```bash
GET /books/api/authors/{id}/
```

**Create Author**
```bash
POST /books/api/authors/
Content-Type: application/json

{
    "name": "Author Name",
    "email": "author@example.com",
    "bio": "Author biography",
    "birth_date": "1980-01-01"
}
```

**Update Author**
```bash
PUT /books/api/authors/{id}/
PATCH /books/api/authors/{id}/
```

**Delete Author**
```bash
DELETE /books/api/authors/{id}/
```

**Search and Order Authors**
```bash
# Search by name or bio
GET /books/api/authors/?search=author_name

# Order by name or birth_date
GET /books/api/authors/?ordering=name
GET /books/api/authors/?ordering=-birth_date
```

### Books API

**List Books**
```bash
GET /books/api/books/
```

**Get Book Details**
```bash
GET /books/api/books/{id}/
```

**Create Book**
```bash
POST /books/api/books/
Content-Type: application/json

{
    "title": "Book Title",
    "isbn": "1234567890123",
    "publication_date": "2023-01-01",
    "price": 29.99,
    "genre": "Fiction",
    "authors": [1, 2]
}
```

**Update Book**
```bash
PUT /books/api/books/{id}/
PATCH /books/api/books/{id}/
```

**Delete Book**
```bash
DELETE /books/api/books/{id}/
```

### Book Filtering

The books API supports advanced filtering using `ModelMultipleChoiceFilter`:

**Filter by Multiple Authors**
```bash
GET /books/api/books/?authors=1&authors=2
```

**Filter by Title (contains)**
```bash
GET /books/api/books/?title=python
```

**Filter by Genre (contains)**
```bash
GET /books/api/books/?genre=fiction
```

**Filter by Price Range**
```bash
GET /books/api/books/?min_price=20&max_price=50
```

**Combine Multiple Filters**
```bash
GET /books/api/books/?authors=1&genre=fiction&min_price=20
```

**Search and Order Books**
```bash
# Search by title or ISBN
GET /books/api/books/?search=python

# Order by title, publication_date, or price
GET /books/api/books/?ordering=title
GET /books/api/books/?ordering=-publication_date
GET /books/api/books/?ordering=price
```

### Custom Book Endpoints

**Books by Genre**
```bash
GET /books/api/books/by_genre/?genre=fiction
```

**Expensive Books (price >= min_price)**
```bash
GET /books/api/books/expensive_books/?min_price=50
```

### Example API Responses

**Author Response**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "A prolific author",
    "birth_date": "1980-01-01"
}
```

**Book Response (Detail)**
```json
{
    "id": 1,
    "title": "Python Programming",
    "authors": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A prolific author",
            "birth_date": "1980-01-01"
        }
    ],
    "isbn": "1234567890123",
    "publication_date": "2023-01-01",
    "price": 29.99,
    "genre": "Programming"
}
```

**Book Response (List)**
```json
{
    "id": 1,
    "title": "Python Programming",
    "authors": ["John Doe"],
    "isbn": "1234567890123",
    "publication_date": "2023-01-01",
    "price": 29.99,
    "genre": "Programming"
}
```

## Key Files

- `books/filters.py`: Contains the `ModelMultipleChoiceFilter` implementation
- `books/models.py`: Defines Book and Author models
- `books/views.py`: Views with filtering logic
- `books/templates/`: HTML templates for the web interface

## Dependencies

- Django
- django-filter
- djangorestframework
- Poetry (for dependency management) 