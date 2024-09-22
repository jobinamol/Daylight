from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('packages/', views.packages, name='packages'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('userindex/', views.userindex, name='userindex'),
    path('userregister/', views.userregister, name='userregister'),
    path('profile/', views.user_view_profile, name='user_view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('rel/',views.rel,name='rel'),
    path('packs/',views.packs,name='packs'),
    path('booking/',views.booking,name='booking'),

]
