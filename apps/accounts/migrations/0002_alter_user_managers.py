# Generated by Django 5.0.1 on 2024-02-06 19:29

import apps.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.accounts.models.BaseUserManager()),
            ],
        ),
    ]