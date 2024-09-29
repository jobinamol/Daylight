from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
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
    menu_items = MenuItem.objects.all()
    return render(request, 'menu_management.html', {'menu_items': menu_items})



def add_menu_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        description = request.POST.get('description', '')
        price = request.POST['price']
        image = request.FILES.get('image')

        menu_item = MenuItem(name=name, category=category, description=description, price=price, image=image)
        menu_item.save()
        return redirect('menu_management')

    return render(request, 'add_menu_item.html')

def edit_menu_item(request, item_id):
    menu_item = MenuItem.objects.get(id=item_id)

    if request.method == 'POST':
        menu_item.name = request.POST['name']
        menu_item.category = request.POST['category']
        menu_item.description = request.POST.get('description', '')
        menu_item.price = request.POST['price']

        if 'image' in request.FILES:
            menu_item.image = request.FILES['image']

        menu_item.save()
        return redirect('menu_management')

    return render(request, 'edit_menu_item.html', {'menu_item': menu_item})

def delete_menu_item(request, item_id):
    menu_item = MenuItem.objects.get(id=item_id)
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
    rooms = Room.objects.all()
    return render(request, 'roommanagement.html', {'rooms': rooms})

# Add a new room
def add_room(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        room_type = request.POST.get('room_type')
        status = request.POST.get('status')
        image = request.FILES.get('image')  # Handling image uploads

        # Create a new Room instance
        room = Room.objects.create(number=number, room_type=room_type, status=status, image=image)
        room.save()

        return redirect('roommanagement')

    return render(request, 'add_rooms.html')

# Edit an existing room
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.number = request.POST.get('number')
        room.room_type = request.POST.get('room_type')
        room.status = request.POST.get('status')

        # Update image if a new one is uploaded
        if request.FILES.get('image'):
            room.image = request.FILES['image']

        room.save()

        return redirect('roommanagement')

    return render(request, 'edit_rooms.html', {'room': room})

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('roommanagement')
    return render(request, 'confirm_delete.html', {'room': room})



