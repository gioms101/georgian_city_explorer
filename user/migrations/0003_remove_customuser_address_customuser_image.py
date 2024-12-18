# Generated by Django 5.0.7 on 2024-12-11 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='default.png', upload_to='products/'),
        ),
    ]
