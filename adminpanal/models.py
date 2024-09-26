from django.db import models
from django.utils import timezone


class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Note: Store hashed passwords in production

    class Meta:
        db_table = 'admin'  # This should match the name of your table in MySQL


class PackageManagement(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    
class Staff(models.Model):
    ROLE_CHOICES = [
        ('frontdesk', 'Front Desk'),
        ('housekeeping', 'Housekeeping'),
        ('culinary', 'Culinary'),
        ('customer_service', 'Customer Service')
    ]
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)  # Allow null values for existing rows
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='staff_images/', default='default.jpg')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name