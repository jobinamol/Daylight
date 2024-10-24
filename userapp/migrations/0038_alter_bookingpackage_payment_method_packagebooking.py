# Generated by Django 5.1 on 2024-10-23 21:22

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0037_rename_email_userdb_emailid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingpackage',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('net_banking', 'Net Banking'), ('upi', 'UPI')], max_length=50),
        ),
        migrations.CreateModel(
            name='PackageBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(default='Default Package', max_length=100)),
                ('number_of_adults', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')], max_length=50)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('confirmation_status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='userapp.userdb')),
            ],
            options={
                'db_table': 'package_bookings',
                'ordering': ['-booking_date'],
            },
        ),
    ]
