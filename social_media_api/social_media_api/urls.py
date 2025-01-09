from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView  

# Make sure you import home view from the correct module
from api.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),  # Use default LoginView 
    path('', home, name='home'),
    path('api/', include('api.urls')),  # Route for API endpoints
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Only serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
