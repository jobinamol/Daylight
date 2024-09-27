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

    

]
