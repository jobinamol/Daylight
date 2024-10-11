from django.db import models
from django.core.validators import MinValueValidator
from userapp.models import *
from staffs.models import *


class Booking(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='booking_entries')
    package = models.ForeignKey(PackageManagement, null=True, blank=True, on_delete=models.CASCADE)  # Allow null for migration
    number_of_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    number_of_children = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    confirmation_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest'} - {self.package.name if self.package else 'No Package'} - {self.booking_date.strftime('%Y-%m-%d %H:%M')}"

    def confirm_booking(self):
        self.confirmation_status = 'confirmed'
        self.save()

    def cancel_booking(self):
        self.confirmation_status = 'canceled'
        self.save()
