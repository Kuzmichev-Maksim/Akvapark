# Generated by Django 5.0.9 on 2024-12-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coral', '0009_remove_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]