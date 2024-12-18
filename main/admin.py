from django.contrib import admin
from django.db import models
from .models import Category, Location, City
from django_json_widget.widgets import JSONEditorWidget

# Register your models here.

admin.site.register(Category)
admin.site.register(City)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
