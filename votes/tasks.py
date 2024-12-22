from celery import shared_task
from django.db.models import Count
from .models import PossibleLocation
from main.models import Location


@shared_task
def check_voting():
    locations = PossibleLocation.objects.annotate(votes_count=Count('votes')).filter(votes_count__gte=1)

    if locations:
        instances_to_save = [
            Location(
                name=location.name,
                city_id=location.city_id,
                address=location.address,
                category_id=location.category_id,
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
        return 'Success!'

    return "There is nothing to add!"
