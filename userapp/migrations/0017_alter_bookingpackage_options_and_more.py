# Generated by Django 5.1 on 2024-10-17 03:04

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0016_remove_bookingpackage_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookingpackage',
            options={'ordering': ['-booking_date']},
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='booking_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='check_in_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='check_out_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookingpackage',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='bookingpackage',
            name='num_adults',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='bookingpackage',
            name='num_children',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='bookingpackage',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('net_banking', 'Net Banking'), ('upi', 'UPI')], max_length=50),
        ),
    ]