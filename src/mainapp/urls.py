from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(info=openapi.Info(title='Help section API', default_version='v0.1', terms_of_service=''))


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

_ADDITIONAL_MODULES = ('help',)


for additional_module in _ADDITIONAL_MODULES:
    module_url = f'{additional_module}/'
    urls_path = f'{additional_module}.urls'
    urlpatterns.append(path(module_url, include((urls_path, additional_module))))
