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

## Key Files

- `books/filters.py`: Contains the `ModelMultipleChoiceFilter` implementation
- `books/models.py`: Defines Book and Author models
- `books/views.py`: Views with filtering logic
- `books/templates/`: HTML templates for the web interface

## Dependencies

- Django
- django-filter
- Poetry (for dependency management) 