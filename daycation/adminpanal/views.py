from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


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
        image = request.FILES.get('image')

        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
        else:
            uploaded_file_url = None 
            
        package = Package(
            name=name,
            price=price,
            description=description,
            duration=duration,
            image=uploaded_file_url
        )
        package.save()
        return redirect('packagemanagement')  # Redirect to the same page to see the updated list

    return render(request, 'packagemanagement.html', {'packages': packages})

def edit_package(request, package_id):
    package = Package.objects.filter(id=package_id).first()
    
    if package is None:
        return redirect('packagemanagement')  # Redirect if package does not exist

    if request.method == 'POST':
        package.name = request.POST['name']
        package.price = request.POST['price']
        package.description = request.POST['description']
        package.duration = request.POST['duration']
        
        if request.FILES.get('image'):
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            package.image = uploaded_file_url
        
        package.save()
        return redirect('packagemanagement')

    return render(request, 'edit_package.html', {'package': package})

def delete_package(request, package_id):
    package = Package.objects.filter(id=package_id).first()
    
    if package:
        package.delete()

    return redirect('packagemanagement')

