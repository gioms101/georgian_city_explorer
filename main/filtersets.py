import django_filters
from .models import Location


class LocationFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city__name')
    category = django_filters.CharFilter(field_name='category__name')

    class Meta:
        model = Location
        fields = ('city', 'category')
