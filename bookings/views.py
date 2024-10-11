from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Booking
from userapp.models import UserDB  # Ensure you import UserDB correctly
from django.contrib.auth.decorators import login_required

@login_required
def create_booking(request):
    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        number_of_adults = request.POST.get('number_of_adults')
        payment_method = request.POST.get('payment_method')
        
        # Validate input here (basic example)
        if not package_name or not number_of_adults or not payment_method:
            return HttpResponse("All fields are required.", status=400)

        # Create the booking
        booking = Booking(
            user=request.user,
            package_name=package_name,
            number_of_adults=number_of_adults,
            payment_method=payment_method
        )
        booking.save()
        return redirect('booking_success')  # Redirect to a success page

    return render(request, 'booking/create_booking.html')

@login_required
def booking_success(request):
    return render(request, 'booking/success.html')

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)  # Fetch bookings for the logged-in user
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()  # Delete the booking
    return redirect('booking_list')
