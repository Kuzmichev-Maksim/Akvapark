# Generated by Django 5.0.9 on 2024-12-15 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coral', '0008_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
