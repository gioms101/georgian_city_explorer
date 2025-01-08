from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.urls import reverse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SubscriptionPlan, Subscription
from .serializers import SubscriptionPlanSerializer, SubscriptionSerializer, CompleteSubscriptionSerializer
from .tasks import get_product_and_plan_id
from .integrate_paypal import PayPalService


class CreateSubscriptionPlanAPIView(CreateAPIView):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        plan = serializer.save()
        get_product_and_plan_id.delay(plan.id)

class CreateSubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription_plan = SubscriptionPlan.objects.get(id=serializer.data['plan_id'])
        paypal_service = PayPalService()
        # user_pk = request.user.pk
        return_url = request.build_absolute_uri(
            reverse('success')
        )
        cancel_url = request.build_absolute_uri(
            reverse('cancel')
        )
        subscription = Subscription.objects.filter(user=request.user)
        if subscription:
            subscription = subscription.first()
            if subscription.expiration_date < now():
                response = paypal_service.create_subscription(subscription_plan.plan_id, return_url, cancel_url)
                return Response(response)
            else:
                return Response({'message': "You already have subscription for this plan."}, status=400)
        else:
            response = paypal_service.create_subscription(subscription_plan.plan_id, return_url, cancel_url)
            return Response(response)


class CompleteSubscriptionAPIView(APIView):
    serializer_class = CompleteSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CompleteSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription_plan = SubscriptionPlan.objects.get(id=serializer.data['plan_id'])
        expire_date = relativedelta(months=subscription_plan.duration) + now()
        Subscription.objects.create(user=request.user, plan_id=serializer.data['plan_id'],
                                    expiration_date=expire_date)
        return Response({'message': "Congratulations, You're subscription has been activated."}, status=200)


class SuccessResponseView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'success': "Congratulations, you have successfully completed your subscription."})


class CancelSubscriptionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Something went wrong.'})
