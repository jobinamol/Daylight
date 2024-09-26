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

def packagemanagement(request):
    packages = PackageManagement.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        image = request.FILES.get('image')

        if not name or not price or float(price) <= 0 or not description or not duration:
            messages.error(request, 'Please fill in all fields correctly.')
            return redirect('packagemanagement')

        try:
            package = PackageManagement(
                name=name,
                price=price,
                description=description,
                duration=duration,
                image=image
            )
            package.save()
            messages.success(request, 'Package added successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('packagemanagement')

    return render(request, 'packagemanagement.html', {'packages': packages})

def edit_package(request, package_id):
    package = get_object_or_404(PackageManagement, id=package_id)

    if request.method == 'POST':
        package.name = request.POST.get('name')
        package.price = request.POST.get('price')
        package.description = request.POST.get('description')
        package.duration = request.POST.get('duration')

        if request.FILES.get('image'):
            package.image = request.FILES['image']  # Update the image if a new one is provided

        if not package.name or not package.price or float(package.price) <= 0 or not package.description or not package.duration:
            messages.error(request, 'Please fill in all fields correctly.')
            return redirect('edit_package', package_id=package.id)

        try:
            package.save()
            messages.success(request, 'Package updated successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('packagemanagement')

    return render(request, 'edit_package.html', {'package': package})

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


