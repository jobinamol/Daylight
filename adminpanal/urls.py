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
    path('packages/edit/<int:package_id>/', views.edit_package, name='edit_package'),

    # URL for deleting a specific package
    path('packages/delete/<int:package_id>/',views. delete_package, name='delete_package'),
    path('package_list/', views.package_list, name='package_list'),  # URL for package list
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category_management/', views.category_management, name='category_management'),
    path('category_management/update/<int:category_id>/', views.update_category, name='update_category'),
    path('get_food_items_by_category/<int:category_id>/', views.get_food_items_by_category, name='get_food_items_by_category'),
    path('bookingmanagament/', views.bookingmanagement, name='bookingmanagement'),



    # other URL patterns
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/update/', views.activity_update, name='activity_update'),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    
    path('admindaycation-packages/', views.daycation_package_management, name='daycation_package_management'),
    path('daycation-packages/edit/<int:package_id>/', views.edit_daycation_package, name='edit_daycation_package'),
    path('daycation-packages/delete/<int:package_id>/', views.delete_daycation_package, name='delete_daycation_package'),
    path('daycation-packages/list/', views.daycation_package_list, name='daycation_package_list'),
    
    path('daycation-packages/', views.daycation_packages, name='daycation_packages'),
    path('daycation-packages/category/<int:category_id>/', views.daycation_category_packages, name='daycation_category_packages'),

    path('daycation/<int:package_id>/', views.daycation_package_details, name='daycation_package_details'),
    path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('package/<int:package_id>/book/', views.book_package, name='book_package'),
    path('package/<int:package_id>/process_booking/', views.process_booking, name='process_booking'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
