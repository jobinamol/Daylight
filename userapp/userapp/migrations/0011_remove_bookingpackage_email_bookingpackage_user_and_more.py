# Generated by Django 5.1 on 2024-10-14 02:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0010_bookingpackage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingpackage',
            name='email',
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userapp.userdb'),
        ),
        migrations.AlterField(
            model_name='bookingpackage',
            name='payment_method',
            field=models.CharField(max_length=50),
        ),
    ]
