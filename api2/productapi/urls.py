"""
URL configuration for productapi project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('metrics', include('django_prometheus.urls')),
]
