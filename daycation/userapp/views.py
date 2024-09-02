from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.utils.datastructures import MultiValueDictKeyError

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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.status == 1:
            auth_login(request, user)
            return redirect('userdashboard')
        else:
            messages.error(request, 'Invalid credentials or account not active')
            return redirect('login')

    return render(request, 'login.html')

# User dashboard view
@login_required
def userdashboard(request):
    return render(request, 'userdashboard.html')

# User registration view
def userregister(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['emailid']
        mobile_number = request.POST['mobilenumber']
        address = request.POST['address']
        city = request.POST['city']
        district = request.POST['district']
        age = request.POST['age']
        sex = request.POST['sex']
        profile_image = request.FILES.get('profile_image')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('userregister')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create profile
        Profile.objects.create(
            user=user,
            mobile_number=mobile_number,
            address=address,
            city=city,
            district=district,
            age=age,
            sex=sex,
            profile_image=profile_image
        )

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'userregister.html')
# View user profile
@login_required
def userviewprofile(request):
    user = request.user
    data = UserDB.objects.filter(username=user.username).first()
    return render(request, 'userviewprofile.html', {'data': data})

# Edit user profile view
@login_required
def usereditprofile(request, id):
    data = get_object_or_404(UserDB, id=id)
    return render(request, 'usereditprofile.html', {'data': data})

# Update user profile view
@login_required
def userupdate(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        mobilenumber = request.POST.get('mobilenumber')
        emailid = request.POST.get('emailid')
        district = request.POST.get('district')

        # Handle image update
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
        except MultiValueDictKeyError:
            file = UserDB.objects.get(id=id).image  # Keep existing image if not updated

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Update the user's details
        UserDB.objects.filter(id=id).update(
            name=name,
            mobilenumber=mobilenumber,
            emailid=emailid,
            district=district,
            username=username,
            password=make_password(password) if password else UserDB.objects.get(id=id).password,
            image=file
        )
        messages.success(request, 'Profile updated successfully!')
        return redirect('userviewprofile')

    return redirect('usereditprofile', id=id)

# Delete user profile view
@login_required
def userdelete(request, id):
    UserDB.objects.filter(id=id).delete()
    messages.success(request, 'User profile deleted successfully.')
    return redirect('home')

# Change password view
@login_required
def userchangepassword(request, id):
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmnewpassword = request.POST.get('confirmnewpassword')

        user = UserDB.objects.filter(id=id).first()
        if user and check_password(oldpassword, user.password):
            if newpassword == confirmnewpassword:
                user.password = make_password(newpassword)
                user.save()
                messages.success(request, 'Password updated successfully!')
                return redirect('userviewprofile')
            else:
                messages.error(request, 'New passwords do not match')
        else:
            messages.error(request, 'Incorrect old password')

    return render(request, 'userchangepassword.html')

# Logout view
@login_required
def userlogout(request):
    auth_logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

# Forgot password view
def userforgotpassword(request):
    return render(request, 'userforgotpassword.html')
