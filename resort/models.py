from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone
import uuid
import random
import string

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    otp_generated_at = models.DateTimeField(blank=True, null=True)  # To track OTP generation time
    username = models.EmailField(max_length=254, unique=True)  # Set username to be the same as email
    first_name = models.CharField(max_length=30)  # Ensure this field exists
    last_name = models.CharField(max_length=30)   # Ensure this field exists
    is_verified = models.BooleanField(default=False)  # Track email verification status
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique token for verification
    password = models.CharField(max_length=128)   # Adjust as necessary

    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = []  # No additional fields required at signup

    def save(self, *args, **kwargs):
        # Ensure username is set to the email before saving
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def generate_otp(self):
        """Generate a random 6-digit OTP."""
        self.email_otp = ''.join(random.choices(string.digits, k=6))
        self.otp_generated_at = timezone.now()  # Set the time when OTP is generated
        self.save()

    def is_otp_valid(self, entered_otp):
        """Check if the entered OTP is valid and not expired."""
        if self.email_otp == entered_otp:
            # Check if OTP is expired (e.g., 5 minutes validity)
            if timezone.now() - self.otp_generated_at <= timezone.timedelta(minutes=5):
                return True
        return False

    def clear_otp(self):
        """Clear the OTP after verification."""
        self.email_otp = None
        self.otp_generated_at = None
        self.save()


class Guest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="guest_profile")

    def __str__(self):
        return f"Guest: {self.user.email}"

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"


class ResortOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="resort_owner_profile")

    def __str__(self):
        return f"Resort Owner: {self.user.email}"

    class Meta:
        verbose_name = "Resort Owner"
        verbose_name_plural = "Resort Owners"

class Resort(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='resort_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ResortPackage(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dynamic_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.resort.name}"


