# Generated by Django 5.0.7 on 2024-12-15 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_comment_parent_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
