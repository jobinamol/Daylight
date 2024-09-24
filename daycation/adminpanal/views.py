from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from userapp.models import*


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

def packagemanagement(request):
    packages = Package.objects.all()
    
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        duration = request.POST['duration']
        image = request.FILES.get('image')  # Handle the uploaded image

        try:
            package = Package(
                name=name,
                price=price,
                description=description,
                duration=duration,
                image=image  # Directly assign image
            )
            package.save()
            messages.success(request, 'Package added successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('packagemanagement')  

    return render(request, 'packagemanagement.html', {'packages': packages})

def editpackage(request, package_id):
    package = Package.objects.filter(id=package_id).first()

    if package is None:
        messages.error(request, 'Package not found.')
        return redirect('packagemanagement')

    if request.method == 'POST':
        package.name = request.POST['name']
        package.price = request.POST['price']
        package.description = request.POST['description']
        package.duration = request.POST['duration']
        
        if request.FILES.get('image'):
            package.image = request.FILES['image']  # Update the image if a new one is provided
        
        try:
            package.save()
            messages.success(request, 'Package updated successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('packagemanagement')  
        
    return render(request, 'editpackage.html', {'package': package})

def delete_package(request, package_id):
    package = Package.objects.filter(id=package_id).first()
    
    if package:
        try:
            package.delete()
            messages.success(request, 'Package deleted successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    else:
        messages.error(request, 'Package not found.')

    return redirect('packagemanagement')


def usermanagement(request):
    # Fetch all users from the UserDB model without checking login status
    users = UserDB.objects.all()

    # Pass the list of users to the template
    return render(request, 'usermanagement.html', {'users': users})