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
    path('check_username/', views.check_username, name='check_username'),

    path('userregister/', views.userregister, name='userregister'),
    path('viewprofile/', views.viewprofile, name='viewprofile'),  # URL for viewing user profile
    path('editprofile/', views.editprofile, name='editprofile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('logout/', views.logout, name='logout'),
    path('rel/', views.rel, name='rel'),
    path('fam/', views.fam, name='fam'),
    path('adv/', views.adv, name='adv'),
    path('lux/', views.lux, name='lux'),
    path('corp/', views.corp, name='corp'),
    path('std/', views.std, name='std'),
    path('well/', views.well, name='well'),
    path('rom/', views.rom, name='rom'),
    path('cel/', views.cel, name='cel'),
    path('packs/', views.packs, name='packs'),
    path('menu/', views.menu, name='menu'),
    path('Restaurants/', views.Restaurants, name='Restaurants'),
    path('rooms/', views.rooms, name='rooms'),
    path('room_inquiry/', views.room_inquiry, name='room_inquiry'),
    path('food_inquiry/', views.food_inquiry, name='food_inquiry'),
    path('booking/', views.booking_view, name='booking'),  # URL for the booking page
]
