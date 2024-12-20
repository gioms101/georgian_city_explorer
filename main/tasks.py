from celery import shared_task
from django.core.cache import cache
from django.db.models import Count
from .models import Location


@shared_task
def popular_locations(cache_key):
    locations = (Location.objects.annotate(views_count=Count('views')).filter(views_count__gt=1)
                         .order_by('-views_count'))
    cached_data = list(locations.values('id', 'name', 'city', 'address', 'image'))
    cache.set(cache_key, cached_data, timeout=60)
    for location in locations:
        location.views.clear()
    return 'Ordered by view count successfully!'
