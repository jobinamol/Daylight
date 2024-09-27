# Generated by Django 5.1 on 2024-09-24 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0006_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='password',
            field=models.CharField(default='your_default_password', max_length=128),
        ),
        migrations.AddField(
            model_name='staff',
            name='username',
            field=models.CharField(default='default_username', max_length=150, unique=True),
        ),
    ]