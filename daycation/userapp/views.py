from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from .models import*
from django.contrib.auth import logout as auth_logout, authenticate, login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .forms import PasswordResetRequestForm 
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking, Payment
from adminpanal.models import*





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

def userdashboard(request):
    if request.user.is_authenticated:
        return render(request, 'userdashboard.html', {'user': request.user})
    return redirect('login')

def userindex(request):
    return render(request, 'userindex.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserDB.objects.get(username=username)
        except UserDB.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['profile_image'] = user.profile_image.url
            user.save()  

            messages.success(request, f'Welcome, {user.name}!')
            return redirect('userindex')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

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

        if UserDB.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('userregister')

        if UserDB.objects.filter(emailid=emailid).exists():
            messages.error(request, 'Email ID already exists.')
            return redirect('userregister')

        hashed_password = make_password(password)

        # Handle profile image
        profile_image_path = 'default.jpg'
        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            profile_image_path = filename

        user_db = UserDB(
            name=name,
            address=address,
            mobilenumber=mobilenumber,
            emailid=emailid,
            district=district,
            age=age,
            sex=sex,
            username=username,
            password=hashed_password,
            profile_image=profile_image_path
        )
        user_db.save()

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'userregister.html')


def viewprofile(request):
    if 'username' not in request.session:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('login')

    user = UserDB.objects.get(username=request.session['username'])
    
    return render(request, 'userapp/viewprofile.html', {'user': user})




def editprofile(request):
    # Check if user is authenticated based on session
    if 'username' not in request.session:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('login')

    # Get the user based on the session username
    try:
        user = UserDB.objects.get(username=request.session['username'])
    except UserDB.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.address = request.POST.get('address')
        user.mobilenumber = request.POST.get('mobilenumber')
        user.emailid = request.POST.get('emailid')
        user.district = request.POST.get('district')
        user.age = request.POST.get('age')
        user.sex = request.POST.get('sex')

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            user.profile_image = filename

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('viewprofile')

    return render(request, 'userapp/editprofile.html', {'user': user})


def changepassword(request):
    # Check if user is authenticated based on session
    if 'username' not in request.session:
        messages.error(request, "You need to be logged in to change your password.")
        return redirect('login')

    # Get the user based on the session username
    try:
        user = UserDB.objects.get(username=request.session['username'])
    except UserDB.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(current_password, user.password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('viewprofile')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

    return render(request, 'userapp/changepassword.html')

 
 
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = UserDB.objects.get(emailid=email)
                # Generate a random token (you can customize this)
                reset_token = get_random_string(30)
                user.reset_token = reset_token
                user.save()
                
                # Send reset email (for now, let's print the link)
                reset_link = f"http://http://localhost:8000/reset-password/{reset_token}/"
                # Send the email
                subject = "Password Reset Request"
                message = f"Hi, please click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."
                from_email = 'jobinamoljaimon2025@mca.ajce.in'
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list)
                
                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('/login/')
            except UserDB.DoesNotExist:
                messages.error(request, 'Email address not found')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

def reset_password(request, token):
    try:
        user = UserDB.objects.get(reset_token=token)
    except UserDB.DoesNotExist:
        messages.error(request, 'Invalid or expired reset token')
        return redirect('/login/')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password and len(password) >= 8:
            user.password = password  # Hash the password in a real-world scenario
            user.reset_token = ''  # Clear the reset token
            user.save()
            messages.success(request, 'Your password has been reset successfully')
            return redirect('/login/')
        else:
            messages.error(request, 'Passwords do not match or are not long enough')
    
    return render(request, 'password_reset.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

# Other views
def rel(request):
    return render(request, 'rel.html')

def fam(request):
    return render(request, 'fam.html')

def adv(request):
    return render(request, 'adv.html')

def lux(request):
    return render(request, 'lux.html')

def corp(request):
    return render(request, 'corp.html')

def std(request):
    return render(request, 'std.html')

def well(request):
    return render(request, 'well.html')

def rom(request):
    return render(request, 'rom.html')

def cel(request):
    return render(request, 'cel.html')

def packs(request):
    packages = Package.objects.all()
    
    return render(request, 'packs.html', {'packages': packages})
def booking(request):
    return render(request, 'booking.html')
    

def menu(request):
    return render(request, 'menu.html')

def rooms(request):
    return render(request, 'rooms.html')
def payment(request):
    return render(request, 'payment.html')



def confirmation(request):
    return render(request, 'confirmation.html')
