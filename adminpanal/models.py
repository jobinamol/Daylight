from django.db import models
from django.utils import timezone
from staffs.models import*
from adminpanal.models import*




class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Note: Store hashed passwords in production

    class Meta:
        db_table = 'admin'  # This should match the name of your table in MySQL
        

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FoodCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#packagemanagement model

class PackageManagement(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=100)  # Example: "2 nights"
    additional_day_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price for additional days
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)

    # Relationships
    
    menu_items = models.ManyToManyField(MenuItem)  # Link multiple menu items to the package
    rooms = models.ManyToManyField(Room)  # Link multiple rooms to the package

    def __str__(self):
        return self.name

    def get_duration_in_days(self):
        """Parse duration string to get the number of nights."""
        try:
            return int(self.duration.split()[0])
        except (ValueError, IndexError):
            return 0 
#packagesamplemodel     
class PackageManagement1(models.Model):
    CATEGORY_CHOICES = [
        ('BASIC', 'Basic Package'),
        ('PREMIUM', 'Premium Package'),
        ('FAMILY', 'Family Package'),
        ('CORPORATE', 'Corporate Package'),
        ('LUXURY', 'Luxury Package'),
        ('ADVENTURE', 'Adventure Package'),
        ('ROMANTIC', 'Romantic Getaway'),
        ('WELLNESS', 'Wellness Retreat'),
        ('GROUP', 'Group Package'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=100)  # Example: "2 nights"
    additional_day_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='BASIC')

    def __str__(self):
        return f"{self.name} - {self.category}"

    def get_duration_in_days(self):
        """Parse duration string to get the number of nights."""
        try:
            return int(self.duration.split()[0])
        except (ValueError, IndexError):
            return 0

    def calculate_total_price(self, additional_days=0):
        """Calculate total price including additional days if any."""
        total_price = self.price
        if additional_days > 0:
            total_price += additional_days * self.additional_day_price
        return total_price

    def get_rooms(self):
        """Return all rooms associated with this package."""
        return self.rooms.all()  # Using the reverse relationship

    def get_menu_items(self):
        """Return all menu items associated with this package."""
        return self.menu_items.all()  # Using the reverse relationship


#staff model  
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