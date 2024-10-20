# Generated by Django 5.1 on 2024-10-19 15:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0039_daycationpackage_available_capacity_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='daycationbooking',
            name='address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='daycationbooking',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='daycationbooking',
            name='full_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='daycationbooking',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='daycationbooking',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
