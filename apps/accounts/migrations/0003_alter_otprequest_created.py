# Generated by Django 5.0.1 on 2024-02-11 13:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_otprequest_id_otprequest_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
