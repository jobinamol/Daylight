# Generated by Django 5.1 on 2024-10-16 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0029_alter_activity_options_remove_activity_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagemanagement',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
