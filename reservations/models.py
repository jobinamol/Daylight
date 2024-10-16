# # In rooms/models.py
# from django.db import models
# from django.utils import timezone
# from django.dispatch import receiver


# class Rooms(models.Model):
#     room_number = models.CharField(max_length=10, unique=True)
#     room_type = models.CharField(max_length=50)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, default='available')  # e.g., 'available', 'occupied'

# class Bookings(models.Model):
#     room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
#     check_in_date = models.DateField()
#     check_out_date = models.DateField()
#     booked_on = models.DateTimeField(auto_now_add=True)

# def update_room_status_on_booking(sender, instance, created, **kwargs):
#     if created:  # Only set to 'occupied' if this is a new booking
#         room = instance.room
#         room.status = 'occupied'
#         room.save()

# # When a booking is deleted (e.g., on checkout), update the room status to 'available'
# @receiver(pre_delete, sender=Booking)
# def update_room_status_on_checkout(sender, instance, **kwargs):
#     room = instance.room
#     room.status = 'available'
#     room.save()