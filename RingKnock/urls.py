from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('lead/', include('lead.urls')),

    path('profile/', include('profile_settings.urls')),

    path('', include('profile_settings.urls')),
    # path('payment/', include('payment.urls')),


    # path("accounts/", include("allauth.urls")),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
