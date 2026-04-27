from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('apps.users.urls')),
    path('api/cars/', include('apps.cars.urls')),
    path('api/kyc/', include('apps.kyc.urls')),
    path('api/accessories/', include('apps.accessories.urls')),

    # ✅ FIXED HERE
    path('api/cart/', include('apps.orders.urls')),

    path('api/chat/', include('apps.chat.urls')),
    path('api/rental/', include('apps.rental.urls')),
    path("api/notifications/", include("apps.notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)