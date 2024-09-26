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

def staffmanagement(request):
    staff_list = Staff.objects.all()
    staff_roles = [role[0] for role in Staff.ROLE_CHOICES]

    if request.method == "POST":
        # Handle form submission for adding/editing staff
        staff_id = request.POST.get('staff_id', None)
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        salary = request.POST.get('salary')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        start_date = request.POST.get('start_date')
        profile_image = request.FILES.get('profile_image')

        # Check if username and other required fields are provided
        if not username or not name:  # Add other necessary checks
            return render(request, 'staffmanagement.html', {
                'staff_list': staff_list,
                'staff_roles': staff_roles,
                'edit_mode': False,
                'staff': None,
                'error': "Username and Name are required fields."
            })

        if staff_id:  # If staff_id is present, update the existing staff member
            staff_member = get_object_or_404(Staff, id=staff_id)
            staff_member.name = name
            staff_member.username = username
            staff_member.password = password
            staff_member.role = role
            staff_member.salary = salary
            staff_member.phone_number = phone_number
            staff_member.email = email
            staff_member.address = address
            staff_member.start_date = start_date
            if profile_image:  # Only update profile image if provided
                staff_member.profile_image = profile_image
            staff_member.save()
        else:  # Add a new staff member
            Staff.objects.create(
                name=name,
                username=username,
                password=password,
                role=role,
                salary=salary,
                phone_number=phone_number,
                email=email,
                address=address,
                start_date=start_date,
                profile_image=profile_image
            )
        return redirect('staffmanagement')  # Redirect to the same page to see the updated staff list

    return render(request, 'staffmanagement.html', {
        'staff_list': staff_list,
        'staff_roles': staff_roles,
        'edit_mode': False,
        'staff': None  # No staff data for the new entry form
    })

def edit_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    staff_roles = [role[0] for role in Staff.ROLE_CHOICES]
    
    if request.method == "GET":
        return render(request, 'staffmanagement.html', {
            'staff_list': Staff.objects.all(),
            'staff_roles': staff_roles,
            'edit_mode': True,
            'staff': staff_member,
            'staff_id': staff_id  # Pass the staff_id to the template
        })

def delete_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    staff_member.delete()
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