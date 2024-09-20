"""
URL configuration for stock_exchange project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

import stock_exchange_app
from stock_exchange_app import  urls
from rest_framework.schemas import get_schema_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Stock Exchange Transaction API",
        default_version='v1',
        description="API for managing users, stocks, and transactions",
        contact=openapi.Contact(email="abdullahkpr22@gmail.com"),
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(stock_exchange_app.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
