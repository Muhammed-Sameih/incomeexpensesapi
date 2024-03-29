from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Income Expenses APIs",
        default_version='v1',
        description="Income Expenses Project backend!",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Users APIs
    path('api/auth/', include('authentication.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/incomes/', include('incomes.urls')),
    path('api/social_auth/', include(('social_auth.urls', 'social_auth'),
                                     namespace="social_auth")),
    path('api/userstats/', include('userstats.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


]
