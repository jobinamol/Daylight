# Generated by Django 5.1 on 2024-10-13 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0024_packagemanagement_rooms'),
        ('staffs', '0008_alter_room_number'),
        ('userapp', '0009_alter_packagebooking_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookingpackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('num_adults', models.IntegerField()),
                ('num_children', models.IntegerField()),
                ('payment_method', models.CharField(max_length=100)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpanal.packagemanagement')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staffs.room')),
            ],
        ),
    ]
