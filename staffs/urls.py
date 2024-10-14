from django.urls import path
from . import views

urlpatterns = [
    path('', views.staffdashboard, name='staffdashboard'),
    path('staff/receptionist/login/', views.receptionist_login, name='receptionist_login'),
    path('staff/chef/login/', views.chef_login, name='chef_login'),
    path('staff/server/login/', views.server_login, name='server_login'),
    path('staff/entertainer/login/', views.entertainer_login, name='entertainer_login'),
    path('staff/concierge/login/', views.concierge_login, name='concierge_login'),
    path('staff/arranger/login/', views.arranger_login, name='arranger_login'),

    # Dashboard URLs for different staff roles
    path('staff/receptionist/dashboard/', views.frontdesk_dashboard, name='frontdesk_dashboard'),
    path('staff/housekeeping/dashboard/', views.housekeep_dashboard, name='housekeep_dashboard'),
    path('staff/kitchen/dashboard/', views.kitchenstaff_dashboard, name='kitchenstaff_dashboard'),
    path('staff/foodbeverage/dashboard/', views.fud_dashboard, name='fud_dashboard'),
    path('staff/entertainment/dashboard/', views.evant_dashboard, name='evant_dashboard'),
    path('staff/guestservice/dashboard/', views.guestservice_dashboard, name='guestservice_dashboard'),
    path('menu_management/', views.menu_management, name='menu_management'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('edit_menu_item/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('manage_special_menu/', views.manage_special_menu, name='manage_special_menu'),
    path('roommanagement/', views.roommanagement, name='roommanagement'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('order-management/',views.order_management_view, name='order_management'),
    path('feedback-management/', views.feedback_management_view, name='feedback_management'),
    path('categories/', views.list_food_categories, name='list_food_categories'),
    path('categories/add/', views.add_food_category, name='add_food_category'),
    path('categories/edit/<int:category_id>/', views.edit_food_category, name='edit_food_category'),
    path('categories/delete/<int:category_id>/', views.delete_food_category, name='delete_food_category'),
   path('admin/bookingmanage/', views.bookingmanage, name='bookingmanage'),
    path('admin/booking_detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),



    

]
