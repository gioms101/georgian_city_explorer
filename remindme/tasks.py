from celery import shared_task
from django.core.mail import send_mail
from .weather_api import WeatherData
from .models import Event


@shared_task
def send_reminder(id_of_event, user_email, city, location_name, event_time):
    obj = WeatherData()
    weather_data = obj.get_weather_data(city)
    subject = f'This is a reminder of going to {location_name} at {event_time.strftime("%H:%M")}'
    message = f"""Stay prepared for your visit with the latest weather update:
                  ----------------------------------------------------------
                    🌤️ Weather: {weather_data['weather_description']}
                    🌡️ Temperature: {weather_data['temp']}°C
                    💧 Humidity: {weather_data['humidity']}%
                    🌬️ Wind Speed: {weather_data['wind_speed_kmh']} km/h
                  ----------------------------------------------------------
                """

    send_mail(
        subject,
        message,
        'settings.EMAIL_HOST_USER',
        [user_email],
        fail_silently=False,
    )

    Event.objects.get(id=id_of_event).delete()  # After sending email to user, deleting event object.
