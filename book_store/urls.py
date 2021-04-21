"""book_receit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.contrib import admin
from django.urls import path, re_path, include


API_VERSION = 'v1'


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^accounts/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('ui.urls')),
    path('book/', include('books.urls')),

    path(f'api/{API_VERSION}/book/', include('books.api.urls')),
    path(f'api/{API_VERSION}/pricing/', include('pricing.api.urls')),
    path(f'api/{API_VERSION}/user/', include('users.api.urls')),
]

# Swagger

SchemaView = get_schema_view(
    openapi.Info(
        title="Book Store API",
        default_version=API_VERSION,
        description="""The `swagger-ui` view can be found [here](/cached/swagger).
The `ReDoc` view can be found [here](/cached/redoc).
The swagger YAML document can be found [here](/cached/swagger.yaml).
        You can log in with you credentials.""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@company.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('redoc-alpha/', SchemaView.with_ui('redoc-alpha', cache_timeout=0), name='schema-redoc-alpha'),
    re_path(r'^cached/swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=None), name='cschema-json'),
    path('cached/swagger/', SchemaView.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    path('cached/redoc/', SchemaView.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
]
