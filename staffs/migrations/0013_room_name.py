# Generated by Django 5.1 on 2024-10-15 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0012_room_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default='Unnamed Room', max_length=100),
        ),
    ]