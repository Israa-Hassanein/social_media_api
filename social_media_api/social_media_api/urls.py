from django.contrib import admin
from django.urls import path, include
from api.views import home, LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('', home, name='home'),
    path('api/', include('api.urls')),  # Route for API endpoints
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Only serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
