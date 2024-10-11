from django.urls import path
from .views import create_booking, booking_list, booking_success, cancel_booking

urlpatterns = [
    path('bookings/create/', create_booking, name='create_booking'),
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/success/', booking_success, name='booking_success'),
    path('bookings/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]
