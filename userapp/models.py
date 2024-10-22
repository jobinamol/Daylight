from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Import models from adminindex and staff apps
from adminpanal.models import* # Import Package from adminindex app
from staffs.models import*
 # Adjust the import according to your structure


class UserDB(models.Model):
    id = models.AutoField(primary_key=True)  # or UUIDField

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
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        unique_together = ('emailid', 'username')  # Ensure unique combination of email and username

    def get_email_field_name(self):
        return 'emailid'

    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=6))


class PackageBooking(models.Model):
    user = models.ForeignKey(UserDB, on_delete=models.CASCADE, related_name='bookings')  # Related name for easier access
    package_name = models.CharField(max_length=100, default="Default Package")
    number_of_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least one adult
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])  # Adding choices for payment method
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmation_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'package_bookings'  # Explicit table name
        ordering = ['-booking_date']  # Default ordering by booking date (latest first)

    def __str__(self):
        return f"{self.user.username} - {self.package_name} - {self.booking_date.strftime('%Y-%m-%d %H:%M')}"
    
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.package}"

    class Meta:
        ordering = ['-booking_date']

    def save(self, *args, **kwargs):
        if not self.id:
            self.booking_date = timezone.now()
        return super(Bookingpackage, self).save(*args, **kwargs)





class EmailVerification(models.Model):
    user = models.ForeignKey(UserDB, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at
