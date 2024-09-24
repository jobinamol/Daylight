from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from .models import UserDB
from django.contrib.auth import logout as auth_logout, authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required



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
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('login')

    user = UserDB.objects.get(username=request.user.username)
    
    return render(request, 'userapp/viewprofile.html', {'user': user})



def edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('login')

    user = UserDB.objects.get(username=request.user.username)

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.address = request.POST.get('address')
        user.mobilenumber = request.POST.get('mobilenumber')
        user.emailid = request.POST.get('emailid')
        user.district = request.POST.get('district')
        user.age = request.POST.get('age')
        user.sex = request.POST.get('sex')

        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            user.profile_image = filename

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('view_profile')

    return render(request, 'userapp/edit_profile.html', {'user': user})


def changepassword(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to change your password.")
        return redirect('login')

    user = UserDB.objects.get(username=request.user.username)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(current_password, user.password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('view_profile')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

    return render(request, 'userapp/change_password.html')


def forgot_password(request):
    if request.method == 'POST':
        emailid = request.POST.get('emailid')
        try:
            user = UserDB.objects.get(emailid=emailid)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [emailid])
            
            messages.success(request, 'Password reset instructions have been sent to your email.')
            return redirect('login')
        except UserDB.DoesNotExist:
            messages.error(request, 'No account found with that email.')

    return render(request, 'forgot_password.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserDB.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, UserDB.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
        
        return render(request, 'password_reset_confirm.html', {'user': user})
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('forgot_password')

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
    return render(request, 'packs.html')

def booking(request):
    return render(request, 'booking.html')
