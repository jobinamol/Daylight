from django.shortcuts import render, redirect, get_object_or_404
from .models import*
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from userapp.models import*
from django.http import HttpResponse



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

#package management
def packagemanagement(request):
    packages = Package.objects.all()  # Retrieve all packages from the database
    
    if request.method == 'POST':  # Handle form submission to add a new package
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        duration = request.POST['duration']
        image = request.FILES.get('image')  # Get the uploaded image, if provided

        try:
            package = Package(
                name=name,
                price=price,
                description=description,
                duration=duration,
                image=image  # Save image if provided
            )
            package.save()  # Save the new package to the database
            messages.success(request, 'Package added successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return redirect('packagemanagement')  # Redirect to the same page to show updated package list

    return render(request, 'packagemanagement.html', {'packages': packages})

def editpackage(request, package_id):
    package = Package.objects.filter(id=package_id).first()  # Retrieve package by ID
    
    if package is None:  # If no package is found, show an error message
        messages.error(request, 'Package not found.')
        return redirect('packagemanagement')

    if request.method == 'POST':  # Handle form submission for updating package details
        package.name = request.POST['name']
        package.price = request.POST['price']
        package.description = request.POST['description']
        package.duration = request.POST['duration']
        
        if request.FILES.get('image'):  # If a new image is uploaded, update it
            package.image = request.FILES['image']
        
        try:
            package.save()  # Save the updated package details
            messages.success(request, 'Package updated successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return redirect('packagemanagement')

    return render(request, 'editpackage.html', {'package': package})

def delete_package(request, package_id):
    package = Package.objects.filter(id=package_id).first()  # Retrieve the package by ID
    
    if package:  # If package exists, delete it
        try:
            package.delete()
            messages.success(request, 'Package deleted successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    else:
        messages.error(request, 'Package not found.')

    return redirect('packagemanagement')