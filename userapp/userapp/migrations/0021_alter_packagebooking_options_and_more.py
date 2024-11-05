# Generated by Django 5.1 on 2024-10-22 13:18

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0020_alter_packagebooking_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='packagebooking',
            options={'ordering': ['-booking_date']},
        ),
        migrations.AlterUniqueTogether(
            name='userdb',
            unique_together={('emailid', 'username')},
        ),
        migrations.AddField(
            model_name='userdb',
            name='emailid',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userdb',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='userdb',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userdb',
            name='reset_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userdb',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Username may only contain letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.@+-]+$')]),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='district',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='mobilenumber',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Mobile number must be between 10 and 15 digits and can optionally start with a "+" sign.', regex='^\\+?\\d{10,15}$')]),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='sex',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterModelTable(
            name='userdb',
            table='users',
        ),
        migrations.DeleteModel(
            name='EmailVerification',
        ),
        migrations.RemoveField(
            model_name='userdb',
            name='email_verification_token',
        ),
        migrations.RemoveField(
            model_name='userdb',
            name='is_email_verified',
        ),
        migrations.RemoveField(
            model_name='userdb',
            name='user',
        ),
    ]