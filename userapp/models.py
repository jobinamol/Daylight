from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
import pyotp  # Required for OTP generation
from django.utils import timezone
from django.utils.text import slugify


class UserDBManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.otp_secret = pyotp.random_base32()  # Generate a secret for OTP
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, email, password, **extra_fields)

class UserDB(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    mobilenumber = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?\d{10,15}$",
                message="Mobile number must be between 10 and 15 digits and can optionally start with a '+' sign.",
            )
        ],
    )
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    sex = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Username may only contain letters, numbers, and @/./+/-/_ characters.",
            )
        ],
    )
    profile_image = models.ImageField(upload_to="profile_images/", default="default.jpg")
    last_login = models.DateTimeField(default=now)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    otp_secret = models.CharField(max_length=16, blank=True, null=True)  # OTP field for 2FA
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="userdb_set",
        related_query_name="userdb",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="userdb_set",
        related_query_name="userdb",
    )

    objects = UserDBManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "name"]

    class Meta:
        db_table = "users"
        unique_together = ("email", "username")

    def get_email_field_name(self):
        return "email"

    def __str__(self):
        return self.username

    def generate_otp(self):
        """Generate a time-based OTP using pyotp."""
        totp = pyotp.TOTP(self.otp_secret)
        return totp.now()

    def verify_otp(self, otp):
        """Verify the OTP entered by the user."""
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)


class PackageManagement(models.Model):
    package_name = models.CharField(max_length=255)
    package_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.package_name



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
class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.room_number








class ResortProfile(models.Model):
    user = models.OneToOneField(UserDB, on_delete=models.CASCADE, related_name="resort_profile")
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)  # Consider adding validation for phone numbers
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # SEO-friendly URL

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Resort Profile'
        verbose_name_plural = 'Resort Profiles'
        db_table = 'userapp_resortprofile'


class ResortImage(models.Model):
    resort = models.ForeignKey(ResortProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='resort_images/')

    def __str__(self):
        return f"Image for {self.resort.name}"

    class Meta:
        verbose_name = 'Resort Image'
        verbose_name_plural = 'Resort Images'
    



