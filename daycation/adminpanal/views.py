from django.shortcuts import render
from .models import Admin
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password:  # Check password (hashed in production)
                # Authentication successful
                return render(request, 'adminindex.html', {'admin': admin})
            else:
                # Incorrect password
                messages.error(request, 'Invalid username or password.')
        except Admin.DoesNotExist:
            # Username does not exist
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'adminlogin.html')


def admin_index(request):
    return render(request, 'adminindex.html')
