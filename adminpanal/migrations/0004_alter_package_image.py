# Generated by Django 5.1 on 2024-09-24 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0003_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]