from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('adminindex/', views.admin_index, name='adminindex'),
    # other URL patterns
]
