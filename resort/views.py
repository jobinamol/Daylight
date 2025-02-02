from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from .models import *
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from django.http import JsonResponse
from .models import CustomUser
from django.conf import settings
import random
import string
from django.utils import timezone

# Create your views here.

def guest_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the email already exists
        if Users1.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': "Email already exists."})

        # Basic validation for password matching
        if password != confirm_password:
            return render(request, 'signup.html', {'error': "Passwords do not match."})

        # Create user
        user = Users1(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)  # Hash the password
        user.verification_token = uuid.uuid4()  # Generate a unique token
        user.save()

        # Send verification email
        send_verification_email(user)

        return redirect('signup_success')  # Redirect to a success page or message
    return render(request, 'signup.html')

def send_verification_email(user):
    token = user.verification_token
    verification_link = f"http://yourdomain.com/verify-email/{token}/"  # Update with your domain
    send_mail(
        'Verify your email',
        f'Click the link to verify your email: {verification_link}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

def verify_email(request, token):
    user = Users1.objects.filter(verification_token=token).first()
    if user:
        user.is_verified = True
        user.verification_token = uuid.uuid4()  # Generate a new token after verification
        user.save()
        return render(request, 'verification_success.html')
    return render(request, 'verification_failed.html')





PROJECT_ID = 'resort-nbwr'
  # Replace with your Dialogflow project ID

def chat_with_bot(request):
    # Get the user message from the request
    user_message = request.GET.get('message', '')

    # Set up Dialogflow session
    session_id = "12345"  # You can use a unique ID for each user
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    # Prepare the text input
    text_input = dialogflow.TextInput(text=user_message, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    # Send the request to Dialogflow
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    bot_reply = response.query_result.fulfillment_text

    # Send the bot's reply back to the user
    return JsonResponse({"response": bot_reply})


def chatbot_page(request):
    return render(request, 'chatbot.html')

def generate_otp():
    """Generate a random 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_via_email(email, otp):
    """Send the OTP to the user's email."""
    subject = 'Email Verification OTP'
    message = f'Your OTP for email verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def send_otp(request):
    """View to handle sending OTP to the user's email."""
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()  # Generate OTP
            user.email_otp = otp  # Store OTP in the user model
            user.otp_generated_at = timezone.now()  # Set the time when OTP is generated
            user.save()  # Save the user with the new OTP
            send_otp_via_email(email, otp)  # Send OTP via email
            return redirect('verify_otp', user_id=user.id)  # Redirect to OTP verification page
        except CustomUser.DoesNotExist:
            return render(request, 'send_otp.html', {'error': 'Email not found'})
    return render(request, 'send_otp.html')

def verify_otp(request, user_id):
    """View to handle verifying the OTP entered by the user."""
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if user.is_otp_valid(entered_otp):  # Check if the OTP is valid
            user.is_email_verified = True  # Mark email as verified
            user.clear_otp()  # Clear OTP after successful verification
            return redirect('home')  # Redirect to home or login page
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid or expired OTP'})
    return render(request, 'verify_otp.html')
