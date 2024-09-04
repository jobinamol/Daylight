from django.urls import path
from . import views

urlpatterns = [
    path('', views.staffdashboard, name='staffdashboard'),
    path('receptionist/login/', views.receptionist_login, name='receptionist_login'),
    path('receptionist/login/', views.receptionist_login, name='receptionist_login'),
    path('chef/login/', views.chef_login, name='chef_login'),
    path('server/login/', views.server_login, name='server_login'),
    path('entertainer/login/', views.entertainer_login, name='entertainer_login'),
    path('concierge/login/', views.concierge_login, name='concierge_login'),
    path('arranger/login/', views.arranger_login, name='arranger_login'),

]
