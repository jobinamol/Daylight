from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Note: Store hashed passwords in production

    class Meta:
        db_table = 'admin'  # This should match the name of your table in MySQL

class Package(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Staff(models.Model):
    ROLE_CHOICES = [
        ('Front Desk', 'Front Desk'),
        ('Housekeeping', 'Housekeeping'),
        ('Culinary', 'Culinary'),
        ('Entertainment', 'Entertainment'),
        ('Maintenance', 'Maintenance'),
        ('Customer Service', 'Customer Service'),
    ]

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    start_date = models.DateField()
    profile_image = models.ImageField(upload_to='staff_images/', blank=True, null=True)

    def __str__(self):
        return self.name