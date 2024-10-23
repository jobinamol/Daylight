from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from adminpanal.models import PackageManagement
from staffs.models import Room
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# User Model
class UserDBManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserDB(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    mobilenumber = models.CharField(max_length=15)
    district = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')

    objects = UserDBManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'  # This tells Django to use the 'users' table


# Package Booking Model
class PackageBooking(models.Model):
    user = models.ForeignKey(UserDB, on_delete=models.CASCADE, related_name='bookings')
    package_name = models.CharField(max_length=100, default="Default Package")
    number_of_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least one adult
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmation_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'package_bookings'  # Explicit table name
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.package_name} - {self.booking_date.strftime('%Y-%m-%d %H:%M')}"


# Booking Package Model
class Bookingpackage(models.Model):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, null=True)  
    num_adults = models.IntegerField(validators=[MinValueValidator(1)])
    num_children = models.IntegerField(validators=[MinValueValidator(0)])
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    package = models.ForeignKey(PackageManagement, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now, editable=False)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    num_rooms = models.IntegerField(default=1)
    food_preference = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.package}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.booking_date = timezone.now()  # Automatically set the booking date
        return super(Bookingpackage, self).save(*args, **kwargs)

