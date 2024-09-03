from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('packages/', views.packages, name='packages'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),  # Updated to 'login_view'
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('userindex/',views.userindex,name='userindex'),
    path('userregister/', views.userregister, name='userregister'),
]
