# Generated by Django 5.1 on 2024-10-18 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0036_remove_daycationpackage_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='daycationpackage',
            name='duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]