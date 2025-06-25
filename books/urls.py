from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for the REST API
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)

app_name = 'books'

urlpatterns = [
    # Template-based URLs (existing)
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    
    # REST API URLs
    path('api/', include(router.urls)),
] 