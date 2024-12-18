from celery import shared_task
from django.db.models import Count
from django.core.cache import cache
from .models import PossibleLocation
from main.models import Location


@shared_task
def check_voting(cache_key):
    locations = PossibleLocation.objects.annotate(votes_count=Count('votes')).filter(votes_count__gt=1)

    if locations:
        instances_to_save = [
            Location(
                name=location.name,
                city=location.city,
                address=location.address,
                category=location.category,
                latitude=location.latitude,
                longitude=location.longitude,
                image=location.image,
                working_hours=location.working_hours,
                description=location.description,
            )
            for location in locations
        ]
        Location.objects.bulk_create(instances_to_save)
        PossibleLocation.objects.all().delete()
        cache.delete(cache_key)
        return 'Success!'

    return "There is nothing to add!"
