from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import FrontDeskCoordinator


def staffdashboard(request):
    return render(request, 'staffdashboard.html')
def receptionist_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's authentication system
        user = authenticate(request, username=username, password=password)
        
        if user is not None and isinstance(user, FrontDeskCoordinator):
            login(request, user)
            return redirect('frontdesk_dashboard')  # Redirect to the admin dashboard or any other page
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'receptionist_login.html')
def chef_login(request):
    return render(request, 'chef_login.html')

def server_login(request):
    return render(request, 'server_login.html')

def entertainer_login(request):
    return render(request, 'entertainer_login.html')

def concierge_login(request):
    return render(request, 'concierge_login.html')

def arranger_login(request):
    return render(request, 'arranger_login.html')

def frontdesk_dashboard(request):
    return render(request, 'frontdesk_dashboard.html')

def housekeep_dashboard(request):
    return render(request,'housekeep_dashboard.html')


def kitchenstaff_dashboard(request):
    return render(request,'kitchenstaff_dashboard.html')

def fud_dashboard(request):
    return render(request,'fud_dashboard.html')

def evant_dashboard(request):
    return render(request,"evant_dashboard.html")

def guestservice_dashboard(request):
    return render(request,"guestservice_dashboard.html")



