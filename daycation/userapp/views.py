from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
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

        try:
            # Retrieve the user from UserDB model using the username
            user_db = UserDB.objects.get(username=username)
            
            # Check if the provided password matches the hashed password in the database
            if check_password(password, user_db.password):
                # Manually log in the user by setting session data
                request.session['user_id'] = user_db.id
                request.session['username'] = user_db.username
                
                # Redirect to the user index page
                return redirect('userindex')
            else:
                messages.error(request, 'Invalid credentials.')

        except UserDB.DoesNotExist:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'login.html')

# User dashboard view
def userdashboard(request):
    return render(request, 'userdashboard.html')

# User index view
def userindex(request):
    return render(request, 'userindex.html')

def userregister(request):
    if request.method == 'POST':
        # Collect form data
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

        # Check if username or email already exists
        if UserDB.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('userregister')
        
        if UserDB.objects.filter(emailid=emailid).exists():
            messages.error(request, 'Email ID already exists.')
            return redirect('userregister')

        # Hash the password before saving
        hashed_password = make_password(password)

        # Handle profile image
        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            profile_image_path = filename
        else:
            profile_image_path = 'default.jpg'

        # Create UserDB entry
        user_db = UserDB(
            name=name,
            address=address,
            mobilenumber=mobilenumber,  # Matches model field
            emailid=emailid,            # Matches model field
            district=district,
            age=age,
            sex=sex,
            username=username,          # Matches model field
            password=hashed_password,   # Save hashed password
            profile_image=profile_image_path
        )

        # Save the UserDB entry
        user_db.save()

        # Provide success message and redirect to login
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'userregister.html')
