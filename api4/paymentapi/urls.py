"""
URL configuration for paymentapi project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/payments/', include('payments.urls')),
    path('metrics', include('django_prometheus.urls')),
]
