# Generated by Django 5.1 on 2024-09-22 22:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0011_alter_userdb_age_alter_userdb_emailid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdb',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
