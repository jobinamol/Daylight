# Generated by Django 5.1 on 2024-10-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanal', '0038_alter_packagefeature_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='daycationpackage',
            name='available_capacity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='daycationpackage',
            name='max_capacity',
            field=models.PositiveIntegerField(),
        ),
    ]