from celery import shared_task
from django.core.cache import cache
from django.db.models import Count, F
from .models import Location


@shared_task
def popular_locations(cache_key):
    locations = (Location.objects.annotate(views_count=Count('views') + F('anonymous_views')).filter(views_count__gte=1)
                         .order_by('-views_count'))
    if locations:
        cached_data = list(locations.values('id', 'name', 'city', 'address', 'image'))
        cache.set(cache_key, cached_data, timeout=20)
        for location in locations:
            location.views.clear()
            location.anonymous_views = 0
            location.save(update_fields=['anonymous_views'])
        return 'Ordered by view count successfully!'
