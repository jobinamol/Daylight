# Generated by Django 5.1 on 2024-09-03 08:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0010_alter_userdb_mobilenumber_alter_userdb_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='emailid',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='mobilenumber',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Mobile number must be between 10 and 15 digits and can optionally start with a "+" sign.', regex='^\\+?\\d{10,15}$')]),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='sex',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='username',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(message='Username may only contain letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.@+-]+$')]),
        ),
        migrations.AlterUniqueTogether(
            name='userdb',
            unique_together={('emailid', 'username')},
        ),
    ]
