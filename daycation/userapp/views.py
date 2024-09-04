from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from .models import UserDB
from django.contrib.auth import logout as auth_logout


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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = UserDB.objects.get(id=user_id)
    return render(request, 'userdashboard.html', {'user': user})

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

# View profile view
def user_view_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = UserDB.objects.get(id=user_id)
    return render(request, 'user_view_profile.html', {'user': user})

# Edit profile view
def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = UserDB.objects.get(id=user_id)
    
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.address = request.POST.get('address')
        user.mobilenumber = request.POST.get('mobilenumber')
        user.emailid = request.POST.get('emailid')
        user.district = request.POST.get('district')
        user.age = request.POST.get('age')
        user.sex = request.POST.get('sex')

        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('user_view_profile')

    return render(request, 'edit_profile.html', {'user': user})

# Forgot password view
def forgot_password(request):
    if request.method == 'POST':
        emailid = request.POST.get('emailid')
        try:
            user = UserDB.objects.get(emailid=emailid)
            # You would typically send a password reset email here
            messages.success(request, 'Password reset instructions have been sent to your email.')
        except UserDB.DoesNotExist:
            messages.error(request, 'No account found with that email.')

    return render(request, 'forgot_password.html')

# Logout view
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
