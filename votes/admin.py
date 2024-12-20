from django.contrib import admin
from django.db import models
from .models import PossibleLocation
from django_json_widget.widgets import JSONEditorWidget
# Register your models here.


@admin.register(PossibleLocation)
class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
