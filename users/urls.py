from django.urls import path
from .views import *

urlpatterns = [
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('singlesignup/', singlesignup, name='singlesignup'),
    path('check_email/', check_email, name='check_email'),
]