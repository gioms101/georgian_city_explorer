from celery import shared_task
from django.core.mail import send_mail

from user.models import CustomUser
from favorites.models import Favorite

@shared_task
def send_email_verification(user_email, link):
    send_mail(
        'Verify Your Email',
        f'Click the link to verify your email: {link}',
        'settings.EMAIL_HOST_USER',
        [user_email],
        fail_silently=False,
    )


@shared_task
def reset_password(user_email, reset_link):
    send_mail(
        "Password Reset Request",
        f"Click the link below to reset your password:\n\n{reset_link}",
        'settings.EMAIL_HOST_USER',
        [user_email],
    )

@shared_task
def merge_favorite_locs(fav_locs, user_pk):
    user = CustomUser.objects.get(pk=user_pk)
    Favorite.objects.bulk_create(
        Favorite(user=user, location_id=location_pk)
        for location_pk in fav_locs
    )
