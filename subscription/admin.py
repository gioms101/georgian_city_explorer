from django.contrib import admin
from .tasks import get_product_and_plan_id
from .models import SubscriptionPlan, Subscription

# Register your models here.

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'duration', 'price', 'currency')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        get_product_and_plan_id.delay(obj.id)

admin.site.register(Subscription)
