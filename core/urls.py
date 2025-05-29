"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.landingpage.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('clients/', include('apps.clients.urls')),
    path('employers/', include('apps.employers.urls')),
    path('department/', include('apps.department.urls')),
    # path('plan/', include('apps.plan.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('chat/', include('apps.chat.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('billings/', include('apps.billings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
