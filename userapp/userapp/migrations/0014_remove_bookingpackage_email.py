# Generated by Django 5.1 on 2024-10-14 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0013_bookingpackage_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingpackage',
            name='email',
        ),
    ]
