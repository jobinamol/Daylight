from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('packages/', views.packs, name='packs'),
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
    path('package/<int:id>/', views.package_details, name='package_details'),
    path('packages/category/<int:category_id>/', views.category_packages, name='category_packages'),
    path('create/<int:id>', views.create_booking, name='create_booking'),
    path('google-login/', views.google_login, name='google_login'),
    path('google-login/callback/', views.google_callback, name='google_callback'),
    path('booking/<int:package_id>/',views. booking_view, name='booking_view'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),



]