from django.urls import path
from . import views
from .views import (
    resort_owner_dashboard,
    create_resort,
    edit_resort,
    create_package,
    edit_package,
    create_room,
    edit_room,
    delete_room,
    edit_owner_profile,
)

urlpatterns = [
    # Staff Login URLs
    path('', views.staffdashboard, name='staffdashboard'),
    path('staff/receptionist/login/', views.receptionist_login, name='receptionist_login'),
    path('staff/chef/login/', views.chef_login, name='chef_login'),
    path('staff/server/login/', views.server_login, name='server_login'),
    path('staff/entertainer/login/', views.entertainer_login, name='entertainer_login'),
    path('staff/concierge/login/', views.concierge_login, name='concierge_login'),
    path('staff/arranger/login/', views.arranger_login, name='arranger_login'),

    
    # Menu Management URLs
    path('menu_management/', views.menu_management, name='menu_management'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('edit_menu_item/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('manage_special_menu/', views.manage_special_menu, name='manage_special_menu'),

    # Room Management URLs
    path('roommanagement/', views.roommanagement, name='roommanagement'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),

    # Order and Feedback Management URLs
    path('order-management/', views.order_management_view, name='order_management'),
    path('feedback-management/', views.feedback_management_view, name='feedback_management'),

    # Food Category Management URLs
    path('categories/', views.list_food_categories, name='list_food_categories'),
    path('categories/add/', views.add_food_category, name='add_food_category'),
    path('categories/edit/<int:category_id>/', views.edit_food_category, name='edit_food_category'),
    path('categories/delete/<int:category_id>/', views.delete_food_category, name='delete_food_category'),

    # Booking Management URLs
    path('admin/bookingmanage/', views.bookingmanage, name='bookingmanage'),
    path('admin/booking_detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),

    # Add any new URLs related to staff functionalities here
    path('edit_owner_profile/', views.edit_owner_profile, name='edit_owner_profile'),
    path('create_package/', views.create_package, name='create_package'),
    
    path('dashboard/', resort_owner_dashboard, name='resort_owner_dashboard'),
    path('create_resort/', create_resort, name='create_resort'),
    path('edit_resort/<int:resort_id>/', edit_resort, name='edit_resort'),
    path('create_package/', create_package, name='create_package'),
    path('edit_package/<int:package_id>/', edit_package, name='edit_package'),
    path('create_room/', create_room, name='create_room'),
    path('edit_room/<int:room_id>/', edit_room, name='edit_room'),
    path('delete_room/<int:room_id>/', delete_room, name='delete_room'),
    path('edit_owner_profile/', edit_owner_profile, name='edit_owner_profile'),
]
    

