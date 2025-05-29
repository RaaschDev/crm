from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('clients/', include('apps.clients.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
] 