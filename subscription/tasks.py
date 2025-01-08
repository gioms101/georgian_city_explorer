from celery import shared_task
import requests
from django.utils.timezone import now

from .models import SubscriptionPlan, Subscription
from .integrate_paypal import PayPalService

@shared_task
def get_product_and_plan_id(subscription_id):
    subscription_plan = SubscriptionPlan.objects.get(id=subscription_id)
    paypal_obj = PayPalService()
    access_token = paypal_obj.get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Prefer': 'return=representation',
    }
    json_data = {
        "name": f"{subscription_plan.name}",
        "description": f"{subscription_plan.description}",
        "type": "SERVICE",
    }
    product_id = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers,
                                                                                            json=json_data).json()['id']
    plan_json_data = {
        "product_id": f"{product_id}",
        "name": f"{subscription_plan.name}",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": subscription_plan.duration
                },
                "tenure_type": "TRIAL",
                "sequence": 1,
            },
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 2,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": f"{subscription_plan.price}",
                        "currency_code": f"{subscription_plan.currency}"
                    }
                }
            }
        ],
        "payment_preferences": {
            "setup_fee": {
                "value": f"{subscription_plan.price}",
                "currency_code": f"{subscription_plan.currency}"
            }
        }
    }
    plan_id = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers,
                                                                                    json=plan_json_data).json()['id']
    subscription_plan.plan_id = plan_id
    subscription_plan.save(update_fields=['plan_id'])


@shared_task
def delete_inactive_subscriptions():
    inactive_subscriptions = Subscription.objects.filter(expiration_date__lt=now())
    if inactive_subscriptions:
        inactive_subscriptions.delete()
        return "Successfully deleted inactive subscriptions."
