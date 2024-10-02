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

class PackageBooking(models.Model):
    package = models.ForeignKey(PackageManagement, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem, through='MenuItemQuantity')
    num_people = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
    additional_requests = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.num_people} people"

class MenuItemQuantity(models.Model):
    booking = models.ForeignKey(PackageBooking, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"





