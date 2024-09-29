from django.db import models

class FrontDeskCoordinator(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'FrontDeskCoordinator'  # Ensure this matches the existing table name
from django.db import models

class Staff(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords in production

    class Meta:
        db_table = 'staff'  # Matches your database table name

    def __str__(self):
        return self.username
    
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks')
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('maintain', 'Maintain'),
        ('occupied', 'Occupied'),
    ]

    number = models.CharField(max_length=5, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)  # Room image

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')  # Status choices

    def __str__(self):
        return f"{self.number} - {self.room_type}"
