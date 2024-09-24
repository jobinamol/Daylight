from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

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

class Package(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='No description available.')  # Default value for description
    category = models.CharField(max_length=100, default='General')  # Default value for category
    image_url = models.CharField(max_length=255, default='images/default.jpg')  # Default image URL

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Booking(models.Model):
    user = models.ForeignKey(UserDB, on_delete=models.CASCADE, null=True)  # Temporarily allow nulls
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)  # Make package optional
    food_items = models.ManyToManyField(FoodItem, blank=True)  # Store selected food items as a Many-to-Many relationship
    room_type = models.CharField(max_length=255, null=True, blank=True)  # Optional
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking by {self.user.username if self.user else 'No user'} - Package: {self.package.name if self.package else 'No package selected'}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    payment_status = models.BooleanField(default=False)  # True if payment is successful
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # Store transaction ID if applicable
    payment_date = models.DateTimeField(auto_now_add=True, null=True)  # Temporarily allow nulls

    def __str__(self):
        return f"Payment for Booking ID: {self.booking.id}"

