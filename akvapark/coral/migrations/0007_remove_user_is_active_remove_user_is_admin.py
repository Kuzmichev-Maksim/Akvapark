# Generated by Django 5.0.9 on 2024-12-10 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coral', '0006_remove_user_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
    ]
