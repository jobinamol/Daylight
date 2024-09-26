# Generated by Django 5.1 on 2024-09-26 12:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0010_remove_staff_address_remove_staff_phone_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='package',
            name='image',
        ),
        migrations.AddField(
            model_name='package',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='package',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(choices=[('Relaxation', 'Relaxation Package'), ('Family', 'Family Fun Package'), ('Adventure', 'Adventure Package'), ('Luxury', 'Luxury Package'), ('Corporate', 'Corporate Retreat Package'), ('Student', 'Student Package')], max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
