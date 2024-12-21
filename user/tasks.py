from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_verification(user_email, link):
    send_mail(
        'Verify Your Email',
        f'Click the link to verify your email: {link}',
        'settings.EMAIL_HOST_USER',
        [user_email],
        fail_silently=False,
    )
