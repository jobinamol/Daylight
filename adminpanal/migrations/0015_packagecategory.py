# Generated by Django 5.1 on 2024-10-08 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0014_packagemanagement_additional_day_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
