from django.urls import path
from . import views

urlpatterns = [
    path('', views.staffdashboard, name='staffdashboard'),
]
