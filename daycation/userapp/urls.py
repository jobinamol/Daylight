# userapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('packages/', views.packages, name='packages'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('userregister/', views.userregister, name='userregister'),
    path('userviewprofile/', views.userviewprofile, name='userviewprofile'),
    path('usereditprofile/<int:id>/', views.usereditprofile, name='usereditprofile'),
    path('userupdateprofile/<int:id>/', views.userupdate, name='userupdateprofile'),
    path('userdeleteprofile/<int:id>/', views.userdelete, name='userdeleteprofile'),
    path('userchangepassword/<int:id>/', views.userchangepassword, name='userchangepassword'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('forgot-password/', views.userforgotpassword, name='userforgotpassword'),


]
