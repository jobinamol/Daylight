# daycation/resort/urls.py
from django.urls import path
from .views import guest_signup, chat_with_bot, chatbot_page, verify_email, send_otp, verify_otp

urlpatterns = [
    path('signup/guest/', guest_signup, name='guest_signup'),  # URL for guest signup
    path('chatbot/', chatbot_page, name='chatbot_page'),      # URL for chatbot page
    path('chatbot/message/', chat_with_bot, name='chat_with_bot'),  # URL for chat with bot
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),  # URL for email verification
    path('send-otp/', send_otp, name='send_otp'),  # URL for sending OTP
    path('verify-otp/<int:user_id>/', verify_otp, name='verify_otp'),  # URL for verifying OTP
]