from openai import OpenAI
from pydantic import BaseModel
from decouple import config


class AboutJourney(BaseModel):
    places: str
    information: str


class TravelMap:
    def __init__(self):
        self.client = OpenAI(
            api_key=config('AI_API_KEY')
        )

    def create_journey_map(self, city, places, language):
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                 "content": f"""You should create Traveler Map of the city which user prompts.Traveler map must includes
                                only this places {places} and nothing else. Places should be only separated by comma.
                                You must return response in {language} language.
                                Ensure the description for each place is concise (e.g., 1-2 sentences).
                                Avoid detailed or lengthy information, and focus on key highlights of the place.
                             """
                 },
                {"role": "user", "content": city},
            ],
            response_format=AboutJourney,
        )
        return response.choices[0].message.parsed
