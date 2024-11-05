# Generated by Django 5.1 on 2024-09-30 15:54

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mobilenumber', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Mobile number must be between 10 and 15 digits and can optionally start with a "+" sign.', regex='^\\+?\\d{10,15}$')])),
                ('emailid', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)])),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('username', models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(message='Username may only contain letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.@+-]+$')])),
                ('profile_image', models.ImageField(default='default.jpg', upload_to='profile_images/')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('reset_token', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'users',
                'unique_together': {('emailid', 'username')},
            },
        ),
    ]