from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from adminpanal.models import *
from userapp.models import *

from django.urls import reverse

from django.http import JsonResponse



def staffdashboard(request):
    return render(request, 'staffdashboard.html')
def receptionist_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's authentication system
        user = authenticate(request, username=username, password=password)
        
        if user is not None and isinstance(user, FrontDeskCoordinator):
            login(request, user)
            return redirect('frontdesk_dashboard')  # Redirect to the admin dashboard or any other page
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'receptionist_login.html')
def chef_login(request):
    return render(request, 'chef_login.html')

def server_login(request):
    return render(request, 'server_login.html')

def entertainer_login(request):
    return render(request, 'entertainer_login.html')

def concierge_login(request):
    return render(request, 'concierge_login.html')

def arranger_login(request):
    return render(request, 'arranger_login.html')

def frontdesk_dashboard(request):
    return render(request, 'frontdesk_dashboard.html')

def housekeep_dashboard(request):
    return render(request,'housekeep_dashboard.html')


def kitchenstaff_dashboard(request):
    return render(request,'kitchenstaff_dashboard.html')

def fud_dashboard(request):
    return render(request,'fud_dashboard.html')

def evant_dashboard(request):
    return render(request,"evant_dashboard.html")

def guestservice_dashboard(request):
    return render(request,"guestservice_dashboard.html")
def menu_management(request):
    # Fetch all menu items with related food category data
    menu_items = MenuItem.objects.select_related('food_category').all()
    
    # Pass the list of menu items to the template
    return render(request, 'menu_management.html', {'menu_items': menu_items})

def add_menu_item(request):
    # Retrieve all food categories
    categories = FoodCategory.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        category_id = request.POST['category']
        
        # Ensure the category exists
        category = get_object_or_404(FoodCategory, id=category_id)

        description = request.POST.get('description', '')
        price = request.POST['price']
        image = request.FILES.get('image')

        # Create and save the new menu item
        menu_item = MenuItem(
            name=name, 
            category=category, 
            description=description, 
            price=price, 
            image=image
        )
        menu_item.save()
        return redirect('menu_management')

    return render(request, 'add_menu_item.html', {'categories': categories})

def edit_menu_item(request, item_id):
    # Retrieve the menu item or return a 404 if not found
    menu_item = get_object_or_404(MenuItem, id=item_id)
    categories = FoodCategory.objects.all()

    if request.method == 'POST':
        menu_item.name = request.POST['name']
        category_id = request.POST['category']

        # Ensure the category exists
        menu_item.category = get_object_or_404(FoodCategory, id=category_id)
        
        menu_item.description = request.POST.get('description', '')
        menu_item.price = request.POST['price']

        if 'image' in request.FILES:
            menu_item.image = request.FILES['image']

        # Save the updated menu item
        menu_item.save()
        return redirect('menu_management')

    return render(request, 'edit_menu_item.html', {'menu_item': menu_item, 'categories': categories})

def delete_menu_item(request, item_id):
    # Retrieve the menu item or return a 404 if not found
    menu_item = get_object_or_404(MenuItem, id=item_id)
    menu_item.delete()
    return redirect('menu_management')


def manage_special_menu(request):
    if request.method == 'POST':
        for item in MenuItem.objects.all():
            is_special = request.POST.get(f'is_special_{item.id}', False) == 'on'
            special_start_date = request.POST.get(f'special_start_{item.id}', None)
            special_end_date = request.POST.get(f'special_end_{item.id}', None)

            item.is_special = is_special
            item.special_start_date = special_start_date
            item.special_end_date = special_end_date
            item.save()
        return redirect('menu_management')  # Redirect to the menu management page

    menu_items = MenuItem.objects.all()
    return render(request, 'manage_special_menu.html', {'menu_items': menu_items})

def roommanagement(request):
    rooms = Room.objects.all().order_by('number')
    return render(request, 'roommanagement.html', {'rooms': rooms})

# Add a new room
def add_room(request):
    if request.method == 'POST':
        try:
            room = Room(
                number=request.POST['number'],
                name=request.POST['name'],  # New field
                category_id=request.POST['category'],
                type=request.POST['type'],
                description=request.POST['description'],
                status=request.POST['status'],
                price=request.POST['price'],
                capacity=request.POST['capacity'],
                available_count=request.POST['available_count'],
            )
            if 'image' in request.FILES:
                room.image = request.FILES['image']
            room.save()
            messages.success(request, 'Room added successfully!')
            return redirect('roommanagement')
        except Exception as e:
            messages.error(request, f'Error adding room: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'add_rooms.html', {'categories': categories})

# Edit an existing room
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        room.number = request.POST.get('number')
        room.category_id = request.POST.get('category')
        room.type = request.POST.get('type')
        room.description = request.POST.get('description')
        room.status = request.POST.get('status')
        room.price = request.POST.get('price')
        room.capacity = request.POST.get('capacity')

        if len(room.number) > 10:  # Adjust based on your model's max_length
            messages.error(request, "Room number is too long. Maximum length is 10 characters.")
            return render(request, 'edit_rooms.html', {'room': room, 'categories': categories})

        try:
            room.save()
            messages.success(request, "Room updated successfully!")
            return redirect('roommanagement')
        except Exception as e:
            messages.error(request, f"An error occurred while updating the room: {str(e)}")
            return render(request, 'edit_rooms.html', {'room': room, 'categories': categories})

    return render(request, 'edit_rooms.html', {'room': room, 'categories': categories})

# Delete a room
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        try:
            room.delete()
            messages.success(request, "Room deleted successfully!")
            return redirect('roommanagement')
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the room: {str(e)}")

    return render(request, 'confirm_delete.html', {'room': room})

def order_management_view(request):
    # Add context data if needed to display orders, etc.
    context = {
        # 'orders': Order.objects.all(), # Example if you have an Order model
    }
    return render(request, 'order_management.html', context)

def feedback_management_view(request):
    # You can add any context data related to feedback if needed
    context = {
        # 'feedbacks': Feedback.objects.all(), # Example if you have a Feedback model
    }
    return render(request, 'feedback_management.html', context)

#catagory
def list_food_categories(request):
    categories = FoodCategory.objects.all()
    return render(request, 'list_food_categories.html', {'categories': categories})

# Add Category
def add_food_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            FoodCategory.objects.create(name=name)
            messages.success(request, 'Category added successfully!')
            return redirect(reverse('list_food_categories'))
    return render(request, 'add_food_category.html')

# Edit Category
def edit_food_category(request, category_id):
    category = get_object_or_404(FoodCategory, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect(reverse('list_food_categories'))
    return render(request, 'edit_food_category.html', {'category': category})

# Delete Category
def delete_food_category(request, category_id):
    category = get_object_or_404(FoodCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect(reverse('list_food_categories'))
    return render(request, 'delete_food_category.html', {'category': category})

def bookingmanage(request):
    # Fetch all booking records
    bookings = Bookingpackage.objects.all()
    # Pass the list of bookings to the template
    return render(request, 'bookingmanage.html', {'bookings': bookings})

def booking_detail(request, booking_id):
    # Fetch the specific booking by ID
    booking = get_object_or_404(Bookingpackage, id=booking_id)
    # Render the booking details in a template
    return render(request, 'booking_detail.html', {'booking': booking})

