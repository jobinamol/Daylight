from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.http import JsonResponse
from .models import userdb 

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def packages(request):
    return render(request, 'packages.html')

def contact(request):
    return render(request, 'contact.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = userdb.objects.get(username=username, password=password, status=1)
            # Store user details in session
            request.session['id'] = user.id
            request.session['name'] = user.name
            request.session['username'] = user.username

            return redirect('userdashboard')
        except userdb.DoesNotExist:
            messages.error(request, 'Invalid user credentials')
            return redirect('userdashboard')

    return render(request, 'login.html')

# User dashboard view
def userdashboard(request):
    return render(request, 'userdashboard.html')

# User registration view
def userregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobilenumber = request.POST.get('mobilenumber')
        emailid = request.POST.get('emailid')
        district = request.POST.get('district')
        image = request.FILES.get('image', None)
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = userdb(
            name=name,
            mobilenumber=mobilenumber,
            emailid=emailid,
            district=district,
            image=image,
            username=username,
            password=password
        )
        data.save()

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'userregister.html')

# View user profile
def userviewprofile(request):
    id = request.session.get('id')
    data = userdb.objects.filter(id=id).first()
    return render(request, 'userviewprofile.html', {'data': data})

# Edit user profile view
def usereditprofile(request, id):
    data = userdb.objects.filter(id=id).first()
    return render(request, 'usereditprofile.html', {'data': data})

# Update user profile view
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
            file = userdb.objects.get(id=id).image  # Keep existing image if not updated

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Update the user's details
        userdb.objects.filter(id=id).update(
            name=name,
            mobilenumber=mobilenumber,
            emailid=emailid,
            district=district,
            username=username,
            password=password,
            image=file
        )
        messages.success(request, 'Profile updated successfully!')
        return redirect('userviewprofile')

    return redirect('usereditprofile', id=id)

# Delete user profile view
def userdelete(request, id):
    userdb.objects.filter(id=id).delete()
    messages.success(request, 'User profile deleted successfully.')
    return redirect('home')

# Change password view
def userchangepassword(request, id):
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmnewpassword = request.POST.get('confirmnewpassword')

        if newpassword == confirmnewpassword:
            if userdb.objects.filter(id=id, password=oldpassword).exists():
                userdb.objects.filter(id=id).update(password=newpassword)
                messages.success(request, 'Password updated successfully!')
                return redirect('userviewprofile')
            else:
                messages.error(request, 'Incorrect old password')
        else:
            messages.error(request, 'New passwords do not match')

    return render(request, 'userchangepassword.html')

# Logout view
def userlogout(request):
    request.session.flush()  # Clear session data
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

# Forgot password view
def userforgotpassword(request):
    return render(request, 'userforgotpassword.html')
