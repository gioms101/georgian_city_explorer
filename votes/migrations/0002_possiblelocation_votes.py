# Generated by Django 5.0.7 on 2024-12-15 10:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='possiblelocation',
            name='votes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
