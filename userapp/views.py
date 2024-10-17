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
from adminpanal.models import*
from staffs.models import*
from bookings.models import*

from django.http import HttpResponseBadRequest
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import os
from decimal import Decimal


from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import requests

# Helper function to convert credentials to a dictionary
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

# Helper function to retrieve Google user info
def get_google_user_info(credentials):
    user_info_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'alt': 'json', 'access_token': credentials.token}
    response = requests.get(user_info_endpoint, params=params)
    
    if response.ok:
        return response.json()
    return None

# Google login view
def google_login(request):
    flow = Flow.from_client_secrets_file(
        'path/to/your/credentials.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(prompt='consent')
    request.session['state'] = state
    return redirect(authorization_url)

# Google callback view
def google_callback(request):
    # Your existing code to fetch user info
    if user_info:
        # Setting session variables
        request.session['username'] = user_info.get('name')
        request.session['email'] = user_info.get('email')
        request.session['profile_image'] = user_info.get('picture')

        # Debug print to verify session data
        print("Username:", request.session.get('username'))
        print("Email:", request.session.get('email'))
        print("Profile Image:", request.session.get('profile_image'))
        
        return redirect('userindex')
    else:
        messages.error(request, 'Google login failed.')
        return redirect('login')



def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def packages(request):
    packages = PackageManagement.objects.all()    

    return render(request, 'packages.html', {'packages': packages})

def packs(request):
    packages = PackageManagement.objects.all()
    categories = Category.objects.all()
    activities = Activity.objects.all()
    food_categories = FoodCategory.objects.all()

    # Search
    search_query = request.GET.get('search')
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        packages = packages.filter(category_id=category_id)

    # Price range
    price_range = request.GET.get('price_range')
    if price_range:
        min_price, max_price = map(lambda x: int(x) if x else None, price_range.split('-'))
        if min_price is not None:
            packages = packages.filter(price__gte=min_price)
        if max_price is not None:
            packages = packages.filter(price__lte=max_price)

    # Duration
    duration = request.GET.get('duration')
    if duration:
        packages = packages.filter(duration__icontains=duration)

    # Activity filter
    activity_id = request.GET.get('activity')
    if activity_id:
        packages = packages.filter(activities__id=activity_id)

    # Rating filter
    rating = request.GET.get('rating')
    if rating:
        packages = packages.filter(rating__gte=int(rating))

    # Food category filter
    food_category_id = request.GET.get('food_category')
    if food_category_id:
        packages = packages.filter(food_categories__id=food_category_id)

    context = {
        'packages': packages,
        'categories': categories,
        'activities': activities,
        'food_categories': food_categories,
        'search_query': search_query,
        'selected_category': category_id,
        'price_range': price_range,
        'duration': duration,
        'selected_activity': activity_id,
        'rating': rating,
        'selected_food_category': food_category_id,
    }
    return render(request, 'packs.html', context)

def category_packages(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    request.GET = request.GET.copy()
    request.GET['category'] = category_id
    return packs(request)

def category_packages(request, category_id):
    selected_category = get_object_or_404(Category, id=category_id)
    packages = PackageManagement.objects.filter(category=selected_category)
    categories = Category.objects.all()
    return render(request, 'packs.html', {
        'packages': packages,
        'categories': categories,
        'selected_category': selected_category,
    })
    
# views.py

from django.shortcuts import render, get_object_or_404
from .models import PackageManagement, Room

# views.py

def package_details(request, id):
    package = get_object_or_404(PackageManagement, id=id)
    # Assuming status can be 'available', 'unavailable', etc.
    available_rooms = Room.objects.filter(status='available')  # Change this as per your actual status values
    return render(request, 'package_details.html', {'package': package, 'available_rooms': available_rooms})



def contact(request):
    return render(request, 'contact.html')

def userdashboard(request):
    if request.user.is_authenticated:
        return render(request, 'userdashboard.html', {'user': request.user})
    return redirect('login')

def userindex(request):
    # Pass session data to the template context
    context = {
        'username': request.session.get('username'),
        'email': request.session.get('email'),
        'profile_image': request.session.get('profile_image')
    }
    return render(request, 'userindex.html', context)

def check_username(request):
    username = request.GET.get('username')
    if UserDB.objects.filter(username=username).exists():
        return JsonResponse({'message': 'Username is already taken.'})
    else:
        return JsonResponse({'message': 'Username is available.'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Clear previous session for the current user
        request.session.flush() 

        # Check if the user is the admin
        if username == 'admin' and password == 'admin':
            request.session['user_type'] = 'admin'
            request.session['username'] = 'admin'
            messages.success(request, 'Welcome, Admin!')
            return redirect('adminindex')
        
        # Staff logins with redirection based on username
        staff_credentials = {
            'frontdesk@gmail.com': ('frontdesk', 'frontdesk_dashboard'),
            'culinary@gmail.com': ('culinary', 'kitchenstaff_dashboard'),
            'customerservice@gmail.com': ('customerservic', 'guestservice_dashboard'),
            'housekeeping@gmail.com': ('housekeeping', 'housekeep_dashboard'),
        }

        # Check if the username is in the staff credentials
        if username in staff_credentials:
            # Verify the password for the respective staff
            expected_password = staff_credentials[username][0]  # Get the expected password
            if password == expected_password:  # Replace with actual password logic if needed
                request.session['user_type'] = username.split('@')[0]  # Track user type based on email
                request.session['username'] = username
                messages.success(request, f'Welcome, {username.split("@")[0].capitalize()} Service!')
                return redirect(staff_credentials[username][1])  # Redirect to respective dashboard
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')

        # Check if the user exists in the UserDB (regular user)
        try:
            user = UserDB.objects.get(username=username)
            if check_password(password, user.password):
                # Check if user already has an active session and clear it
                _invalidate_user_sessions(user.id, 'user')

                # Start a new session for the user
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['profile_image'] = user.profile_image.url
                request.session['user_type'] = 'user'  # Track the type of user
                messages.success(request, f'Welcome, {user.name}!')
                return redirect('userindex')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        except UserDB.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')



def _invalidate_user_sessions(user_id, user_type):
    """Helper function to invalidate all active sessions for a given user or staff."""
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if user_type == 'user' and data.get('user_id') == user_id:
            session.delete()
        elif user_type == 'staff' and data.get('staff_id') == user_id:
            session.delete()

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




def Restaurants(request):
    menu = MenuItem.objects.all()  # Fetch all menu items

    return render(request, 'Restaurants.html',{'menu': menu})
    

def menu(request):
    menu = MenuItem.objects.all()
    categories = FoodCategory.objects.all()  # Fetch all food categories

    return render(request, 'menu.html', {
        'menu': menu,
        'categories': categories,
    })

def rooms(request):
    # Fetch available rooms
    available_rooms = Room.objects.filter(status='available')
    return render(request, 'rooms.html', {'rooms': available_rooms})


def room_inquiry(request):
    if request.method == 'POST':
        response = request.POST.get('response')
        if response == 'yes':
            # Redirect to the available rooms page
            return redirect('rooms')  # Ensure you have this URL mapped in your urls.py
        else:
            # Redirect to the food inquiry page
            return redirect('food_inquiry')  # Ensure you have this URL mapped in your urls.py
            
    return render(request, 'room_inquiry.html')
def food_inquiry(request):
    # Assuming the package_id is available in some way, e.g., from session or a query
    package_id = 1  # You need to dynamically fetch this value
    
    return render(request, 'food_inquiry.html', {
        'package_id': package_id
    })
    


def create_booking(request,id):
    
    package = get_object_or_404(PackageManagement, id=id)
    rooms = Room.objects.filter(status='available')
    
    return render(request, 'create_booking.html', {
        'package': package,
        'rooms': rooms,
    })

def booking_view(request, package_id):
    package = get_object_or_404(PackageManagement, id=package_id)

    if request.method == 'POST':
        # Collect form data
        booking_info = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'num_adults': request.POST.get('num_adults'),
            'num_children': request.POST.get('num_children'),
            'num_rooms': request.POST.get('num_rooms'),
            'food_preference': request.POST.get('food_preference'),
            'payment_method': request.POST.get('payment_method'),
        }

        # Validate data completeness
        if not all(booking_info.values()):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'create_booking.html', {'package': package})

        num_rooms = int(booking_info['num_rooms'])

        # Check room availability
        available_rooms = package.rooms.filter(status='available', available_count__gte=num_rooms)
        if not available_rooms.exists():
            messages.error(request, 'Insufficient rooms available for the selected package.')
            return render(request, 'create_booking.html', {'package': package})

        # Calculate total amount
        num_adults = int(booking_info['num_adults'])
        num_children = int(booking_info['num_children'])
        total_amount = (Decimal(num_adults) + (Decimal(num_children) * Decimal('0.5'))) * package.price * Decimal(num_rooms)

        # Update room availability
        room = available_rooms.first()  # Assuming one room type per booking
        room.available_count -= num_rooms
        if room.available_count == 0:
            room.status = 'occupied'
        room.save()

        # Create a new booking
        booking = Bookingpackage.objects.create(
            first_name=booking_info['first_name'],
            last_name=booking_info['last_name'],
            email=booking_info['email'],
            phone=booking_info['phone'],
            num_adults=num_adults,
            num_children=num_children,
            num_rooms=num_rooms,
            package=package,
            food_preference=booking_info['food_preference'],
            payment_method=booking_info['payment_method'],
            total_amount=total_amount,
        )

        messages.success(request, 'Booking successful!')
        return redirect('booking_success', booking_id=booking.id)
    
    # Render the booking form if it's a GET request or if there's an error
    return render(request, 'create_booking.html', {'package': package})

def booking_success(request, booking_id):
    booking = get_object_or_404(Bookingpackage, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})
