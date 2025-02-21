from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userapp.urls')),
    path('', include('adminpanal.urls')),
    path('staffs/', include('staffs.urls')),
    path('accounts/', include('allauth.urls')),
    path('resort/', include('resort.urls')),
    path('recommend/', include('recommender.urls')),  # ✅ Ensure this is correctly included
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
