# # In rooms/views.py
# from django.shortcuts import render, redirect
# from .models import*
# from django.utils import timezone
# from django.http import HttpResponse


# def book_room(request, room_id):
#     room = Rooms.objects.get(id=room_id)
#     if room.status == 'available':
#         Bookings.objects.create(
#             room=room,
#             check_in_date=timezone.now().date(),
#             check_out_date=timezone.now().date() + timezone.timedelta(days=1)  # Adjust dates as needed
#         )
#         room.status = 'occupied'
#         room.save()
#     return redirect('booking_success')

# def check_out(request, booking_id):
#     booking = Bookings.objects.get(id=booking_id)
#     room = booking.room
#     room.status = 'available'
#     room.save()
#     booking.delete()
#     return redirect('check_out_success')

# def book_room(request, room_id):
#     room = get_object_or_404(Rooms, id=room_id)
#     if room.status == 'available':
#         check_in_date = timezone.now().date()
#         check_out_date = check_in_date + timezone.timedelta(days=1)  # Example of 1-day booking
#         Bookings.objects.create(
#             room=room,
#             check_in_date=check_in_date,
#             check_out_date=check_out_date
#         )
#         return HttpResponse("Room booked successfully!")
#     else:
#         return HttpResponse("Sorry, this room is not available.")

# # In rooms/views.py

# def room_list(request):
#     rooms = Rooms.objects.all()
#     return render(request, 'rooms/room_list.html', {'rooms': rooms})

# # In rooms/views.py

# def check_out(request, booking_id):
#     booking = get_object_or_404(Bookings, id=booking_id)
#     booking.delete()  # Automatically updates the room to "available" through the signal
#     return HttpResponse("Checked out successfully!")

