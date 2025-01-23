from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import UserDB
import random

# Email validation view
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        exists = UserDB.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})

# Phone validation view
def validate_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        exists = UserDB.objects.filter(mobilenumber=phone).exists()
        return JsonResponse({'exists': exists})

# User registration view
def userregister(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email already exists
        if UserDB.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'userregister.html')

        # Send OTP for email verification
        otp = random.randint(100000, 999999)
        send_mail(
            'Email Verification',
            f'Your OTP for verification is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Store OTP in session
        request.session['otp'] = otp
        request.session['account_type'] = account_type
        request.session['email'] = email
        request.session['password'] = make_password(password)  # Hash the password

        messages.success(request, 'OTP sent to your email for verification!')
        return redirect('verify_email')  # Redirect to OTP verification page

    return render(request, 'userregister.html')

def verify_email(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == str(request.session.get('otp')):
            # Create the user after successful verification
            user = UserDB(
                account_type=request.session.get('account_type'),
                email=request.session.get('email'),
                password=request.session.get('password'),
            )
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_email.html')

    return render(request, 'verify_email.html')  # Create a template for OTP input

# Google login view
def google_login(request):
    flow = Flow.from_client_secrets_file(
        'path/to/your/credentials.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(prompt='consent')
    request.session['state'] = state
    return redirect(authorization_url)

# Google callback view
def google_callback(request):
    user_info = get_google_user_info(credentials)  # Ensure you have this function defined
    if user_info:
        request.session['username'] = user_info.get('name')
        request.session['email'] = user_info.get('email')
        request.session['profile_image'] = user_info.get('picture')
        return redirect('userindex')
    else:
        messages.error(request, 'Google login failed.')
        return redirect('login')

# Other views remain unchanged...

