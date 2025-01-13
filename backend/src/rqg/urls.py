"""
URL configuration for rqg project.

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
from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from quotes import views as quotes_views

router = routers.DefaultRouter()
router.register(prefix=r'quotes', viewset=quotes_views.QuoteViewSet, basename='quotes')

urlpatterns = [
    # Django REST Framework
    path(route='', view=include(router.urls)),
    path(route='api-auth/', view=include('rest_framework.urls', namespace='rest_framework')),
    # DRF Spectacular
    path(route='api/schema/', view=SpectacularAPIView.as_view(), name='schema'),
    # Optional DRF Spectacular UI:
    path(route='api/schema/swagger-ui/', view=SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(route='api/schema/redoc/', view=SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Default
    path(route='admin/', view=admin.site.urls),
]
