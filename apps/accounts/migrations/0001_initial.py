# Generated by Django 5.0.1 on 2024-02-05 20:35

import apps.accounts.models
import django.contrib.auth.validators
import django.utils.timezone
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('phone_number', models.CharField(error_messages={'unique': 'phone number is duplicated'}, max_length=15, unique=True, validators=[apps.accounts.models.PhoneNumberValidator()], verbose_name='phone number')),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, max_length=500, null=True, quality=99, scale=None, size=[200, 200], upload_to='avatar', validators=[apps.accounts.models.validate_image_extension], verbose_name='avatar')),
                ('personal_code', models.CharField(error_messages={'unique': 'personal code is duplicated'}, max_length=20, unique=True, verbose_name='personal code')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('gender', models.CharField(choices=[('M', 'male'), ('F', 'female')], max_length=10, verbose_name='gender')),
                ('firstname', models.CharField(blank=True, max_length=150, null=True, verbose_name='first name')),
                ('lastname', models.CharField(blank=True, max_length=150, null=True, verbose_name='last name')),
                ('last_otp_verify', models.DateField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]