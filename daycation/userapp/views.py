from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from .models import UserDB

# Home view
def home(request):
    return render(request, 'home.html')

# About view
def about(request):
    return render(request, 'about.html')

# Blog view
def blog(request):
    return render(request, 'blog.html')

# Packages view
def packages(request):
    return render(request, 'packages.html')

# Contact view
def contact(request):
    return render(request, 'contact.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('userindex')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

# User dashboard view
def userdashboard(request):
    return render(request, 'userdashboard.html')

# User index view
def userindex(request):
    return render(request, 'userindex.html')

# User registration view
def userregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobilenumber = request.POST.get('mobilenumber')
        emailid = request.POST.get('emailid')
        district = request.POST.get('district')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        profile_image = request.FILES.get('profile_image')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('userregister')

        # Create User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=emailid
        )

        # Create UserDB entry
        user_db = UserDB(
            user=user,
            name=name,
            address=address,
            mobile_number=mobilenumber,
            email_id=emailid,
            district=district,
            age=age,
            sex=sex
        )

        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            user_db.profile_image = filename

        user_db.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'userregister.html')
