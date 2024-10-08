from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
# Import models from adminindex and staff apps
from adminpanal.models import* # Import Package from adminindex app
from staffs.models import*

class UserDB(models.Model):
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

    class Meta:
        db_table = 'users'
        unique_together = ('emailid', 'username')  # Ensure unique combination of email and username

    def get_email_field_name(self):
        return 'emailid'


class PackageBooking(models.Model):
    package = models.ForeignKey(PackageManagement, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    menu_items = models.ManyToManyField(MenuItem, through='MenuItemQuantity', related_name='bookings')
    num_people = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
    check_in_date = models.DateField(null=True, blank=True)  # Allow null values
    check_out_date = models.DateField(null=True, blank=True)  # Allow null values
    additional_requests = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.num_people} people from {self.check_in_date} to {self.check_out_date}"

    def calculate_total_price(self):
        """Calculate total price based on selected package, room, menu items, and duration."""
        duration = (self.check_out_date - self.check_in_date).days
        base_price = self.package.price + (self.room.price * self.num_rooms)
        
        # Calculate the price based on the number of nights in the package
        package_duration = self.package.get_duration_in_days()
        
        # Determine additional days if check-in and check-out exceed package duration
        additional_days = max(0, duration - package_duration)
        
        # Total price calculation
        total = base_price + (self.package.additional_day_price * additional_days)

        # Add menu item quantities
        menu_item_quantities = self.menuitemquantity_set.all()
        for menu_item_quantity in menu_item_quantities:
            total += menu_item_quantity.menu_item.price * menu_item_quantity.quantity

        self.total_price = total
        self.save()

    def save(self, *args, **kwargs):
        """Override save method to calculate total price before saving."""
        self.calculate_total_price()
        super().save(*args, **kwargs)


class MenuItemQuantity(models.Model):
    booking = models.ForeignKey(PackageBooking, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"





