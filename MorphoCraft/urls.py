"""
URL configuration for MorphoCraft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('MorphoCraft.apps.public.urls')),
    path('admin', views.admin_index, name='admin'),
    path('admin/', views.admin_index, name='admin'),
    path('admin/home', views.admin_index, name='admin'),
    path('admin/users', views.admin_users, name='admin_users'),
    path('admin/users/action=<str:action>', views.admin_users, name='admin_users'),
    path('admin/logs', views.admin_logs, name='admin_logs'),
    path('admin/logs/action=<str:action>', views.admin_logs, name='admin_logs'),
    path('admin/reviews', views.admin_reviews, name='admin_reviews'),
    path('admin/reviews/action=<str:action>', views.admin_reviews, name='admin_reviews'),
    path('admin/orders', views.admin_orders, name='admin_orders'),
    path('admin/orders/action=<str:action>', views.admin_orders, name='admin_orders'),
    path('admin/orderitems', views.admin_orderitems, name='admin_orderitems'),
    path('admin/orderitems/action=<str:action>', views.admin_orderitems, name='admin_orderitems'),
    path('admin/shipping', views.admin_shipping, name='admin_shipping'),
    path('admin/shipping/action=<str:action>', views.admin_shipping, name='admin_shipping'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
