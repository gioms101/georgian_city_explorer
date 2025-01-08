import base64
import requests
from decouple import config


class PayPalService:
    def __init__(self):
        self.CLIENT_ID = config('PAYPAL_CLIENT_ID')
        self.CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')
        self.headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'PayPal-Request-Id': 'SUBSCRIPTION-21092019-001',
            'Prefer': 'return=representation',
        }

    def get_access_token(self):
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        data = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {0}".format(base64.b64encode((self.CLIENT_ID + ":" + self.CLIENT_SECRET).encode()).decode())
        }
        token = requests.post(url, data, headers=headers)
        return token.json()['access_token']

    def create_subscription(self, plan_id, return_url, cancel_url):
        json = {
            "plan_id": plan_id,
            'application_context': {'return_url': return_url, 'cancel_url': cancel_url},
        }
        response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions', headers=self.headers,
                                 json=json)
        return response.json()
