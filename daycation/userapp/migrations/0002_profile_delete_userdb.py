# Generated by Django 5.1 on 2024-09-01 22:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('sex', models.CharField(max_length=10)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='userdb',
        ),
    ]
