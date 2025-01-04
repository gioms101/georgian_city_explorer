import requests
from decouple import config

""""
This is used to collect current weather data when sending reminder email to user.
"""


class WeatherData:
    def __init__(self):
        self.api_key = config('WEATHER_API_KEY')

    def get_weather_data(self, city):
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city},GE&APPID={self.api_key}').json()
        response['main']['temp'] = self.kelvin_to_celsius(response['main']['temp'])
        parsed_data = self.parse_data(response)
        return parsed_data

    def kelvin_to_celsius(self, kelvin):
        return round(kelvin - 273.15, 1)

    def parse_data(self, response):
        new_response = {'weather_description': response['weather'][0]['description'], 'temp': response['main']['temp'],
                        'humidity': response['main']['humidity'], 'wind_speed_kmh':  round(response['wind']['speed'] * 3.6, 2)}
        return new_response

