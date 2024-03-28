# Generated by Django 5.0.1 on 2024-03-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_sentsms_reasons_sentsms_reason'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otprequest',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='sentsms',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='user',
            name='monthly_price',
            field=models.PositiveBigIntegerField(default=1000000, verbose_name='monthly price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sentsms',
            name='reason',
            field=models.CharField(choices=[('CM', 'custom message')], max_length=50, verbose_name='reason'),
        ),
    ]