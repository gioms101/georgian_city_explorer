from openai import OpenAI
from pydantic import BaseModel


class AboutJourney(BaseModel):
    places: str
    information: str


class TravelMap:
    def __init__(self):
        self.client = OpenAI(
            api_key='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'
        )

    def create_journey_map(self, city, places, language):
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                 "content": f"""You should create Traveler Map of the city which user prompts. This is places {places}
                        Where from you should make Traveler Map.This is Language you should return response {language}.
                             Ensure the description for each place is concise (e.g., 1-2 sentences).
                             Avoid detailed or lengthy information, and focus on key highlights of the place.
                             """
                 },
                {"role": "user", "content": city},
            ],
            response_format=AboutJourney,
        )
        return response.choices[0].message.parsed
