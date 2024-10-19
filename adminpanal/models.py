from django.db import models
from django.utils import timezone
from staffs.models import*
from userapp.models import*
from .models import*
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User




class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Note: Store hashed passwords in production

    class Meta:
        db_table = 'admin'  # This should match the name of your table in MySQL
        

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name




#packagemanagement model
class Activity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Activities"

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Food Categories"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PackageManagement(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    image = models.ImageField(upload_to='packages/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    food_categories = models.ManyToManyField(FoodCategory, blank=True)
    menu_items = models.ManyToManyField(MenuItem, blank=True)
    rooms = models.ManyToManyField('staffs.Room', related_name='packages')
    activities = models.ManyToManyField(Activity, blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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






@receiver(post_save, sender=PackageManagement)
def update_category_count_on_save(sender, instance, **kwargs):
    if instance.category:
        instance.category.update_count()

@receiver(post_delete, sender=PackageManagement)
def update_category_count_on_delete(sender, instance, **kwargs):
    if instance.category:
        instance.category.update_count()
        


from decimal import Decimal

# Main DaycationPackage model
class DaycationPackage(models.Model):
    name = models.CharField(max_length=100)  # Name of the package
    description = models.TextField()  # Detailed description of the package
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the package
    max_capacity = models.IntegerField()  # Maximum capacity (e.g., number of guests)
    duration = models.CharField(max_length=100, blank=True, null=True)  # Duration (e.g., '2 hours', '1 day')
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='packages'
    )  # Link to Category model
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)  # Optional image for the package

    def __str__(self):
        return self.name


# PackageFeature model, linked to DaycationPackage
class PackageFeature(models.Model):
    package = models.ForeignKey(DaycationPackage, related_name='features', on_delete=models.CASCADE)  # Package relation
    name = models.CharField(max_length=100)  # Name of the feature (e.g., Free Wi-Fi, Pool Access)

    def __str__(self):
        return f"{self.package.name} - {self.name}"

    class Meta:
        verbose_name = 'Package Feature'
        verbose_name_plural = 'Package Features'
        ordering = ['package', 'name']


# PackageAddon model, linked to DaycationPackage
class PackageAddon(models.Model):
    package = models.ForeignKey(DaycationPackage, related_name='addons', on_delete=models.CASCADE)  # Package relation
    name = models.CharField(max_length=100)  # Name of the addon (e.g., Spa Access)
    description = models.TextField()  # Description of the addon
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the addon

    def __str__(self):
        return f"{self.package.name} - {self.name}"


# DaycationBooking model, connects to DaycationPackage and selected PackageAddon(s)
class DaycationBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    package = models.ForeignKey(DaycationPackage, on_delete=models.CASCADE)  # Link to the selected daycation package
    date = models.DateField()  # Date of the booking
    guests = models.IntegerField()  # Number of guests
    addons = models.ManyToManyField(PackageAddon, blank=True)  # Multiple addons can be selected
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price including addons
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for booking creation
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')  # Status of the booking (default: pending)

    def __str__(self):
        return f"{self.user.username} - {self.package.name} on {self.date}"

