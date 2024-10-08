from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('adminindex/', views.admin_index, name='adminindex'),
    path('packagemanagement/', views.packagemanagement, name='packagemanagement'),
    path('packages/edit/<int:package_id>/', views.editpackage, name='editpackage'), 
    path('packages/delete/<int:package_id>/', views.delete_package, name='delete_package'), 
    path('usermanagement/', views.usermanagement, name='usermanagement'),

    # other URL patterns
]
