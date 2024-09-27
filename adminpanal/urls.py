from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('logout/', views.logout_view, name='logout'),

    path('adminindex/', views.admin_index, name='adminindex'),
    
    
    path('usermanagement/', views.usermanagement, name='usermanagement'),
    path('staffmanagement/', views.staff_management, name='staffmanagement'),
    path('add_staff/', views.add_staff, name='add_staff'),

    path('staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    
    path('packagemanagement/', views.packagemanagement, name='packagemanagement'),

    # URL for editing a specific package
    path('packages/edit/<int:package_id>/',views. edit_package, name='edit_package'),

    # URL for deleting a specific package
    path('packages/delete/<int:package_id>/',views. delete_package, name='delete_package'),

    # other URL patterns
]
