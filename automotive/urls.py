from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.cars.urls')),
    path('api/', include('apps.kyc.urls')),  
    path("api/", include("apps.accessories.urls")),
    path("api/", include("apps.chat.urls")),# 🔥 VERY IMPORTANT
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)