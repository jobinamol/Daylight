# Generated by Django 5.1 on 2024-10-11 12:34

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0008_rename_num_adults_packagebooking_number_of_adults_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='packagebooking',
            options={'ordering': ['-booking_date']},
        ),
        migrations.AlterField(
            model_name='packagebooking',
            name='number_of_adults',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='packagebooking',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')], max_length=50),
        ),
        migrations.AlterField(
            model_name='packagebooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='userapp.userdb'),
        ),
        migrations.AlterModelTable(
            name='packagebooking',
            table='package_bookings',
        ),
    ]