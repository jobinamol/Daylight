from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User  # Ensure this is correct
from django.contrib import messages




def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email exists in the database
        if User.objects.filter(email=email).exists():
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['email'] = email  # Store email for verification

            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to send OTP: {str(e)}'})

        return JsonResponse({'status': 'error', 'message': 'Email not registered.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp == str(request.session.get('otp')):
            del request.session['otp']  # Clear OTP after verification
            del request.session['email']
            return JsonResponse({'status': 'success', 'message': 'OTP verified successfully.'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def singlesignup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('account_type')

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'User already exists.'})

        # Create and save user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = True  # Activate account immediately
        user.save()

        return JsonResponse({'status': 'success', 'message': 'User registered successfully.'})

    return render(request, 'SingleSignup.html')


def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
