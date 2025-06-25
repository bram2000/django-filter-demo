import django_filters
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    authors = django_filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.all(),
        method='filter_authors',
        label='Authors'
    )
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    def filter_authors(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(authors__in=value).distinct()
    
    class Meta:
        model = Book
        fields = ['title', 'genre', 'authors', 'min_price', 'max_price']    