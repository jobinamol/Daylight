from django.db import models
from adminpanal.models import*  
from staffs.models import *   
from django.db.models import Q



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
    


def get_default_category():
    from adminpanal.models import Category
    return Category.objects.get_or_create(name='Standard')[0].id

# Define TYPE_CHOICES before the Room class
TYPE_CHOICES = [
    ('single', 'Single'),
    ('double', 'Double'),
    ('suite', 'Suite'),
    ('deluxe', 'Deluxe'),
    ('family', 'Family'),
]

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]

    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, default="Unnamed Room")  # Added default value
    category = models.ForeignKey(
        'adminpanal.Category',
        on_delete=models.PROTECT,
        related_name='rooms',
        default=get_default_category
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='single')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    capacity = models.PositiveIntegerField(default=1)
    available_count = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.number}) - {self.category.name} - ₹{self.price}"

    class Meta:
        app_label = 'staffs'
    
    @property
    def is_available(self):
        return self.available_count > 0 and self.status == 'available'

class FoodCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='menu_items')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name
