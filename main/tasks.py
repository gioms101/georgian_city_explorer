from celery import shared_task
from django.core.cache import cache
from django.db.models import Count
from .models import Location


@shared_task
def popular_locations(cache_key):
    popular_locations = Location.objects.annotate(views_count=Count('views')).order_by('-views_count')
    cached_data = list(popular_locations.values('id', 'name', 'city', 'address', 'image'))
    cache.set(cache_key, cached_data, timeout=60)
    for location in popular_locations:
        location.views.clear()
    return 'Ordered by view count successfully!'
