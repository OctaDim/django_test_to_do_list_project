"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include  # Added include
from django.conf.urls.static import static  # Added
from django.conf import settings  # Added


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.router")),  # Added
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Added
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Added

if not settings.DEBUG:  # Plug template, if url was not found, also define in settings MIDDLEWARE and INSTALLED_APPS
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
