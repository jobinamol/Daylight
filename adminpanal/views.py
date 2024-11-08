from django.shortcuts import render, redirect, get_object_or_404
from .models import*
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from userapp.models import*
from staffs.models import*

from django.http import HttpResponse
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_GET, require_POST
from django.db import transaction
from django.db.models import Sum
from django.urls import reverse


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import DaycationPackage, PackageAddon, DaycationBooking, Wishlist
from decimal import Decimal
import traceback
import sys
from django.utils.dateparse import parse_date
import logging
logger = logging.getLogger(__name__)

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password: 
                return render(request, 'adminindex.html', {'admin': admin})
            else:
                messages.error(request, 'Invalid username or password.')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'adminlogin.html')

def logout_view(request):
    logout(request)
    return redirect('login') 


def admin_index(request):
    return render(request, 'adminindex.html')



def usermanagement(request):
    # Fetch all users from the UserDB model without checking login status
    users = UserDB.objects.all()

    # Pass the list of users to the template
    return render(request, 'usermanagement.html', {'users': users})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff

def staff_management(request):
    staff_list = Staff.objects.all()  # Retrieve all staff members
    return render(request, 'staffmanagement.html', {'staff_list': staff_list})

def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Handle password securely in production
        role = request.POST.get('role')
        
        # Check for existing staff with the same email
        if Staff.objects.filter(email=email).exists():
            messages.error(request, 'A staff member with this email already exists.')
            return redirect('add_staff')

        # Create and save new staff member
        staff = Staff(name=name, email=email, password=password, role=role)
        staff.save()
        messages.success(request, 'Staff added successfully.')
        return redirect('staffmanagement')

    return render(request, 'add_staff.html')

def edit_staff(request, staff_id):
    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        messages.error(request, 'Staff member not found.')
        return redirect('staffmanagement')

    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.email = request.POST.get('email')
        staff.role = request.POST.get('role')
        if request.POST.get('password'):
            staff.password = request.POST.get('password')  # Update password if provided
        if request.FILES.get('profile_image'):
            staff.profile_image = request.FILES.get('profile_image')
        staff.save()
        messages.success(request, 'Staff updated successfully.')
        return redirect('staffmanagement')

    return render(request, 'edit_staff.html', {'staff': staff})

def delete_staff(request, staff_id):
    try:
        staff = Staff.objects.get(id=staff_id)
        staff.delete()
        messages.success(request, 'Staff deleted successfully.')
    except Staff.DoesNotExist:
        messages.error(request, 'Staff member not found.')
    
    return redirect('staffmanagement')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PackageManagement, Category, Room, Activity
from decimal import Decimal

def packagemanagement(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            name = request.POST['name']
            price = Decimal(request.POST['price'])
            description = request.POST['description']
            duration = request.POST['duration']
            category_id = request.POST['category']
            
            # Create new package
            package = PackageManagement(
                name=name,
                price=price,
                description=description,
                duration=duration,
                category_id=category_id
            )
            
            # Handle image uploads
            if 'image' in request.FILES:
                package.image = request.FILES['image']
            if 'room_image' in request.FILES:
                package.room_image = request.FILES['room_image']
            
            package.save()
            
            # Handle many-to-many relationships
            activity_ids = request.POST.getlist('activities')
            package.activities.set(activity_ids)
            
            room_ids = request.POST.getlist('rooms')
            package.rooms.set(room_ids)
            
            messages.success(request, f'Package "{package.name}" has been added successfully.')
            return redirect('packagemanagement')
        except Exception as e:
            messages.error(request, f'Error adding package: {str(e)}')

    # GET request: render the form
    packages = PackageManagement.objects.all().prefetch_related('rooms', 'activities')
    categories = Category.objects.all()
    activities = Activity.objects.all()
    rooms = Room.objects.all()

    context = {
        'packages': packages,
        'categories': categories,
        'activities': activities,
        'rooms': rooms,
    }
    return render(request, 'packagemanagement.html', context)

def edit_package(request, package_id):
    package = get_object_or_404(PackageManagement, id=package_id)
    
    if request.method == 'POST':
        # Your existing code for handling POST requests
        pass
    else:
        # Prepare context for GET requests
        categories = Category.objects.all()
        activities = Activity.objects.all()
        rooms = Room.objects.all()

        context = {
            'package': package,
            'categories': categories,
            'activities': activities,
            'rooms': rooms,
        }
        return render(request, 'edit_package.html', context)

def delete_package(request, package_id):
    package = get_object_or_404(PackageManagement, id=package_id)

    if request.method == 'POST':
        try:
            package.delete()
            messages.success(request, 'Package deleted successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('packagemanagement')

    return render(request, 'deletepackage.html', {'package': package})

def package_list(request):
    categories = Category.objects.all()
    packages = packagemanagement.objects.all()  # Assuming you have a Package model

    context = {
        'categories': categories,
        'packages': packages,
    }
    return render(request, 'daycation_package_list.html', context)


def category_management(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_image = request.FILES.get('image')  # Get the image file
        if category_name:
            Category.objects.create(name=category_name, image=category_image)
        return redirect('category_management')
    return render(request, 'category_management.html', {'categories': categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')  # Handle uploaded image
        Category.objects.create(name=name, image=image)
        return redirect('category_list')
    return render(request, 'add_category.html')

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        image = request.FILES.get('image')  # Retrieve image file, if provided
        if image:
            category.image = image  # Update image if provided
        category.save()
        return redirect('category_management')
    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_management')

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_image = request.FILES.get('image')
        if category_name:
            category.name = category_name
        if category_image:
            category.image = category_image  # Update image if provided
        category.save()
        return redirect('category_management')
    return render(request, 'update_category.html', {'category': category})

def get_food_items_by_category(request, category_id):
    food_items = MenuItem.objects.filter(category_id=category_id)
    food_items_data = [{'id': item.id, 'name': item.name} for item in food_items]
    return JsonResponse(food_items_data, safe=False)

def bookingmanagement(request):
    # Fetch all booking records with related package and user data
    bookings = DaycationBooking.objects.select_related('package', 'user').all()
    
    # Pass the list of bookings to the template
    return render(request, 'bookingmanagement.html', {'bookings': bookings})



def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'activity_list.html', {'activities': activities})

def activity_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Activity.objects.create(name=name)
            messages.success(request, 'Activity created successfully.')
            return redirect('activity_list')
        else:
            messages.error(request, 'Activity name is required.')
    return render(request, 'activity_form.html')

def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            activity.name = name
            activity.save()
            messages.success(request, 'Activity updated successfully.')
            return redirect('activity_list')
        else:
            messages.error(request, 'Activity name is required.')
    return render(request, 'activity_form.html', {'activity': activity})

def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully.')
        return redirect('activity_list')
    return render(request, 'activity_confirm_delete.html', {'activity': activity})





def daycation_package_management(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        max_capacity = request.POST.get('max_capacity')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        features = request.POST.getlist('features[]')
        addon_names = request.POST.getlist('addon_name[]')
        addon_prices = request.POST.getlist('addon_price[]')
        addon_descriptions = request.POST.getlist('addon_description[]')

        # Ensure required fields are not empty
        if all([name, description, price, duration, max_capacity, category_id]):
            try:
                # Validate and parse fields
                price = Decimal(price)
                max_capacity = int(max_capacity)

                # Get the related category
                category = Category.objects.get(id=category_id)
                
                # Create the Daycation Package
                package = DaycationPackage.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    duration=duration,
                    max_capacity=max_capacity,
                    category=category,
                    image=image
                )
                
                # Add features to the package
                for feature in features:
                    if feature:  # Ensure non-empty feature names
                        PackageFeature.objects.create(
                            package=package,
                            name=feature,
                        )
                
                # Add add-ons to the package
                for addon_name, addon_price, addon_description in zip(addon_names, addon_prices, addon_descriptions):
                    if addon_name and addon_price:  # Ensure non-empty add-on names and prices
                        PackageAddon.objects.create(
                            package=package,
                            name=addon_name,
                            price=Decimal(addon_price),  # Convert to Decimal
                            description=addon_description or ""  # Add default empty description if none
                        )
                
                # Success message
                messages.success(request, 'Daycation package created successfully.')
                return redirect('daycation_package_list')

            except ValueError:
                messages.error(request, 'Invalid input. Please check your entries.')
            except Category.DoesNotExist:
                messages.error(request, 'Selected category does not exist.')
        else:
            messages.error(request, 'All fields are required.')
    
    # Fetch categories and packages to display on the form
    categories = Category.objects.all()
    packages = DaycationPackage.objects.all()  # Fetch all packages for listing
    return render(request, 'daycation_package_management.html', {'categories': categories, 'packages': packages})

def edit_daycation_package(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    
    if request.method == 'POST':
        package.name = request.POST.get('name')
        package.description = request.POST.get('description')
        package.price = Decimal(request.POST.get('price'))
        package.duration = request.POST.get('duration')
        package.max_capacity = int(request.POST.get('max_capacity'))
        package.category_id = request.POST.get('category')
        
        if 'image' in request.FILES:
            package.image = request.FILES['image']
        
        package.save()

        # Update features
        package.features.all().delete()
        features = request.POST.getlist('features[]')
        for feature in features:
            if feature:
                PackageFeature.objects.create(package=package, name=feature, description="")

        # Update add-ons
        package.addons.all().delete()
        addon_names = request.POST.getlist('addon_name[]')
        addon_prices = request.POST.getlist('addon_price[]')
        addon_descriptions = request.POST.getlist('addon_description[]')
        for name, price, description in zip(addon_names, addon_prices, addon_descriptions):
            if name and price:
                PackageAddon.objects.create(
                    package=package,
                    name=name,
                    price=Decimal(price),
                    description=description
                )

        messages.success(request, 'Daycation package updated successfully.')
        return redirect('daycation_package_list')
    
    categories = Category.objects.all()
    return render(request, 'edit_daycation_package.html', {'package': package, 'categories': categories})

def delete_daycation_package(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Daycation package deleted successfully.')
        return redirect('daycation_package_list')
    
    return render(request, 'delete_daycation_package.html', {'package': package})

def daycation_package_list(request):
    packages = DaycationPackage.objects.all()
    return render(request, 'daycation_package_list.html', {'packages': packages})

def daycation_packages(request):
    packages = DaycationPackage.objects.all()
    categories = Category.objects.all()

    # Get filter parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    price_range = request.GET.get('price_range')
    duration = request.GET.get('duration')

    # Apply filters
    if category_id:
        packages = packages.filter(category_id=category_id)
    
    if search_query:
        packages = packages.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        packages = packages.filter(price__gte=min_price, price__lte=max_price)
    
    if duration:
        min_duration, max_duration = map(int, duration.split('-'))
        packages = packages.filter(duration__gte=min_duration, duration__lte=max_duration)

    # Check if packages are in user's wishlist
    if request.user.is_authenticated:
        wishlist_packages = Wishlist.objects.filter(user=request.user).values_list('package_id', flat=True)
    else:
        wishlist_packages = request.session.get('wishlist', [])

    for package in packages:
        package.is_in_wishlist = package.id in wishlist_packages

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(packages, 9)  # Show 9 packages per page
    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    context = {
        'packages': packages,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'price_range': price_range,
        'duration': duration,
    }

    return render(request, 'daycation_package.html', context)

def daycation_category_packages(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    request.GET = request.GET.copy()
    request.GET['category'] = category_id
    return daycation_packages(request)

def daycation_package_details(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    
    future_bookings = DaycationBooking.objects.filter(
        package=package,
        date__gte=timezone.now().date()
    ).values('date').annotate(total_guests=Sum('num_adults') + Sum('num_children'))

    context = {
        'package': package,
        'future_bookings': list(future_bookings),
    }
    return render(request, 'day_packs_details.html', context)

@login_required
def book_package(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    addons = PackageAddon.objects.filter(package=package)
    context = {
        'package': package,
        'addons': addons,
        'razorpay_key': settings.RAZORPAY_KEY_ID,

    }
    return render(request, 'book_package.html', context)

@login_required
def process_booking(request, package_id):
    """Process booking for a selected package"""
    if request.method == 'POST':
        try:
            logger.info(f"Processing booking for package {package_id}")
            package = get_object_or_404(DaycationPackage, id=package_id)
            
            # Parse and validate the booking date
            booking_date_str = request.POST.get('booking_date')
            try:
                booking_date = parse_date(booking_date_str)
                if not booking_date:
                    raise ValueError("Invalid date format")
            except ValueError:
                return JsonResponse({'error': 'Invalid booking date format'}, status=400)
            
            # Calculate the total price based on adults and children
            num_adults = int(request.POST.get('num_adults', 0))
            num_children = int(request.POST.get('num_children', 0))
            total_price = Decimal(package.price) * (num_adults + (num_children * Decimal('0.5')))
            
            # Handle package addons
            addon_ids = request.POST.getlist('addons')
            addons = PackageAddon.objects.filter(id__in=addon_ids)
            for addon in addons:
                total_price += Decimal(addon.price)
            
            # Create booking
            booking = DaycationBooking.objects.create(
                package=package,
                user=request.user if request.user.is_authenticated else None,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                date=booking_date,
                num_adults=num_adults,
                num_children=num_children,
                food_preference=request.POST.get('food_preference'),
                total_price=total_price,
                status='pending',
                payment_status='unpaid'
            )
            booking.addons.set(addons)
            
            # Create Razorpay order
            razorpay_order = client.order.create({
                'amount': int(total_price * 100),
                'currency': 'INR',
                'payment_capture': '1'
            })
            booking.razorpay_order_id = razorpay_order['id']
            booking.save()
            
            return JsonResponse({
                'id': booking.id,
                'order_id': razorpay_order['id'],
                'amount': int(total_price * 100),
                'currency': 'INR',
                'key': settings.RAZORPAY_KEY_ID,
            })
        except Exception as e:
            logger.error(f"Error processing booking: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def payment_callback(request):
    """Handle payment callback from Razorpay"""
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        }

        try:
            booking = DaycationBooking.objects.get(razorpay_order_id=order_id)
            client.utility.verify_payment_signature(params_dict)
            booking.razorpay_payment_id = payment_id
            booking.razorpay_signature = signature
            booking.status = 'confirmed'
            booking.payment_status = 'paid'
            booking.save()
            return JsonResponse({'status': 'success', 'booking_id': booking.id})
        except Exception as e:
            logger.error(f"Payment verification failed: {str(e)}")
            return JsonResponse({'status': 'failure'}, status=400)

    return JsonResponse({'status': 'invalid request'}, status=400)

@require_GET
def check_availability(request):
    """Check availability of package on a specific date"""
    date = request.GET.get('date')
    package_id = request.GET.get('package_id')
    guests = int(request.GET.get('guests', 0))

    package = get_object_or_404(DaycationPackage, id=package_id)
    bookings = DaycationBooking.objects.filter(date=date, package_id=package_id, status__in=['confirmed', 'pending'])
    booked_capacity = bookings.aggregate(total=Sum('num_adults') + Sum('num_children'))['total'] or 0
    available_capacity = package.max_capacity - booked_capacity

    return JsonResponse({'available_capacity': available_capacity, 'is_available': available_capacity >= guests})

@login_required
def booking_view(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    addons = PackageAddon.objects.filter(package=package)

    user_info = {
        'name': request.user.get_full_name(),
        'mobilenumber': request.user.userdb.mobilenumber if hasattr(request.user, 'userdb') else '',
        'emailid': request.user.email,
        'address': request.user.userdb.address if hasattr(request.user, 'userdb') else '',
    }

    context = {
        'package': package,
        'addons': addons,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'user_info': user_info,
    }

    return render(request, 'book_package.html', context)

@login_required
def booking_history(request):
    bookings = DaycationBooking.objects.filter(user=request.user).order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        bookings = bookings.filter(
            Q(booking_reference__icontains=query) |
            Q(package__name__icontains=query) |
            Q(status__icontains=query)
        )
    
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'booking_history.html', context)

@login_required
def booking_confirmation(request, booking_id):
    """Display booking confirmation details"""
    booking = get_object_or_404(DaycationBooking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
@require_POST
def cancel_booking(request, booking_id):
    """Cancel a booking if allowed"""
    booking = get_object_or_404(DaycationBooking, id=booking_id, user=request.user)
    
    if booking.can_be_cancelled:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking successfully cancelled.')
    else:
        messages.error(request, 'Booking cannot be cancelled.')

    return redirect('booking_history')

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            # Retrieve the payment data
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # Verify the payment signature
            try:
                client.utility.verify_payment_signature(params_dict)
            except:
                return JsonResponse({'status': 'fail', 'message': 'Payment verification failed'}, status=400)

            # If verification is successful, update the booking
            booking = DaycationBooking.objects.get(razorpay_order_id=order_id)
            booking.razorpay_payment_id = payment_id
            booking.razorpay_signature = signature
            booking.payment_status = 'paid'
            booking.status = 'confirmed'
            booking.save()

            return JsonResponse({'status': 'success', 'message': 'Payment verified successfully'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=405)

@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(DaycationBooking, id=booking_id, user=request.user)
    
    if booking.can_be_cancelled():
        if booking.cancel_and_refund():
            messages.success(request, 'Booking successfully cancelled. Refund has been initiated.')
        else:
            messages.error(request, 'Booking cancellation failed. Please contact support.')
    else:
        messages.error(request, 'This booking cannot be cancelled due to the cancellation policy.')

    return redirect('booking_detail', booking_id=booking_id)



def check_booking(request):
    if request.method == 'POST':
        booking_reference = request.POST.get('booking_reference')
        if booking_reference:
            booking = DaycationBooking.objects.filter(booking_reference=booking_reference).first()
            if booking:
                request.session['booking_reference'] = booking_reference
                return redirect('booking_history')
            else:
                messages.error(request, 'No booking found with that reference.')
        else:
            messages.error(request, 'Please enter a booking reference.')
    return redirect('booking_history')

def booking_detail(request, booking_id):
    booking = get_object_or_404(DaycationBooking, booking_reference=booking_id)
    return render(request, 'booking_details1.html', {'booking': booking})

def cancel_booking(request, booking_reference):
    booking = get_object_or_404(DaycationBooking, booking_reference=booking_reference)
    if booking.can_be_cancelled:
        if booking.cancel_and_refund():
            messages.success(request, "Booking cancelled successfully. Refund initiated.")
        else:
            messages.error(request, "Unable to cancel booking. Please contact support.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    return redirect('booking_history')

def check_booking(request):
    if request.method == 'POST':
        booking_reference = request.POST.get('booking_reference')
        if booking_reference:
            booking = DaycationBooking.objects.filter(booking_reference=booking_reference).first()
            if booking:
                request.session['booking_reference'] = booking_reference
                return redirect('booking_detail', booking_reference=booking_reference)
            else:
                messages.error(request, 'No booking found with that reference.')
        else:
            messages.error(request, 'Please enter a booking reference.')
    return redirect('booking_history')

@login_required
@require_POST
def toggle_wishlist(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, package=package)
        if not created:
            wishlist_item.delete()
        is_in_wishlist = created
    else:
        wishlist = request.session.get('wishlist', [])
        if package_id in wishlist:
            wishlist.remove(package_id)
            is_in_wishlist = False
        else:
            wishlist.append(package_id)
            is_in_wishlist = True
        request.session['wishlist'] = wishlist
        request.session.modified = True
    
    return JsonResponse({
        'status': 'success',
        'is_in_wishlist': is_in_wishlist
    })

@login_required
def wishlist(request):
    if request.user.is_authenticated:
        # Fetch wishlist items for authenticated users
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('package')
        packages = [item.package for item in wishlist_items]
    else:
        # Fetch wishlist items from session for non-authenticated users
        wishlist = request.session.get('wishlist', [])
        packages = DaycationPackage.objects.filter(id__in=wishlist)
    
    context = {
        'packages': packages,
        'is_wishlist_page': True  # Add this flag
    }
    return render(request, 'wishlist.html', context)

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = data.get('rating')
            feedback = data.get('feedback')
            booking_id = data.get('booking_id')  # Get booking ID

            # Save feedback to the database
            Feedback.objects.create(rating=rating, feedback=feedback, booking_id=booking_id)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
























































