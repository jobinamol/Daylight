from django.shortcuts import render, redirect, get_object_or_404
from .models import*
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from userapp.models import*
from staffs.models import*

from django.http import HttpResponse
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required





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
    return render(request, 'your_template.html', context)


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
    # Fetch all booking records
    bookings = Bookingpackage.objects.all()
    # Pass the list of bookings to the template
    return render(request, 'bookingmanage.html', {'bookings': bookings})



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
    activities = Activity.objects.all()

    # Get filter parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    price_range = request.GET.get('price_range')
    days = request.GET.get('days')
    rating = request.GET.get('rating')
    activity_id = request.GET.get('activity')

    # Apply filters
    if category_id:
        packages = packages.filter(category_id=category_id)
    
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        if max_price:
            packages = packages.filter(price__gte=min_price, price__lte=max_price)
        else:
            packages = packages.filter(price__gte=min_price)
    
    if days:
        if days == '5+':
            packages = packages.filter(duration__gte=5)
        else:
            packages = packages.filter(duration=int(days))
    
    if rating:
        packages = packages.filter(rating__gte=int(rating))
    
    if activity_id:
        packages = packages.filter(activities__id=activity_id)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(packages, 9)  # 9 packages per page
    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    context = {
        'packages': packages,
        'categories': categories,
        'activities': activities,
        'selected_category': category_id,
        'search_query': search_query,
        'price_range': price_range,
        'days': days,
        'rating': rating,
        'selected_activity': activity_id,
        'is_paginated': packages.has_other_pages(),
        'page_obj': packages,
    }

    return render(request, 'daycation_packages.html', context)

def daycation_category_packages(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    request.GET = request.GET.copy()
    request.GET['category'] = category_id
    return daycation_packages(request)

def daycation_package_details(request, package_id):
    package = get_object_or_404(DaycationPackage, id=package_id)
    features = package.features.all()
    addons = package.addons.all()
    
    context = {
        'package': package,
        'features': features,
        'addons': addons,
    }
    return render(request, 'daycation_package_details.html', context)

@login_required
def book_package(request, package_id):
    if request.method == 'POST':
        package = get_object_or_404(DaycationPackage, id=package_id)
        date = request.POST.get('date')
        guests = int(request.POST.get('guests'))
        addon_ids = request.POST.getlist('addons')
        
        # Calculate total price
        total_price = package.price * Decimal(guests)
        addons = PackageAddon.objects.filter(id__in=addon_ids)
        for addon in addons:
            total_price += addon.price
        
        # Create booking
        booking = DaycationBooking.objects.create(
            user=request.user,
            package=package,
            date=date,
            guests=guests,
            total_price=total_price
        )
        booking.addons.set(addons)
        
        # Redirect to payment page
        return redirect('payment', booking_id=booking.id)
    
    return redirect('package_details', package_id=package_id)

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(DaycationBooking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Process payment (dummy)
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Your booking has been confirmed!')
        return redirect('booking_history')
    
    return render(request, 'payment.html', {'booking': booking})

@login_required
def booking_history(request):
    bookings = DaycationBooking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_history.html', {'bookings': bookings})

