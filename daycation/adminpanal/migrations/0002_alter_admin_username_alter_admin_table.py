# Generated by Django 5.1 on 2024-09-04 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterModelTable(
            name='admin',
            table='admin',
        ),
    ]