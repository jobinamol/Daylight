from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
# Import models from adminindex and staff apps
from adminpanal.models import* # Import Package from adminindex app
from staffs.models import*

class UserDB(models.Model):
    name = models.CharField(max_length=255)
    mobilenumber = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message='Mobile number must be between 10 and 15 digits and can optionally start with a "+" sign.'
            )
        ]
    )
    emailid = models.EmailField(unique=True)  # Ensure unique email
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999)
        ]
    )
    sex = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ]
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$', 
                message='Username may only contain letters, numbers, and @/./+/-/_ characters.'
            )
        ]
    )
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    password = models.CharField(max_length=128)  # Ensure hashed password
    last_login = models.DateTimeField(default=timezone.now)  # Add last_login field
    reset_token = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'users'
        unique_together = ('emailid', 'username')  # Ensure unique combination of email and username

    def get_email_field_name(self):
        return 'emailid'






