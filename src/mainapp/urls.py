from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    info=openapi.Info(title='Help section API', default_version='v0.1'), public=True, permission_classes=(AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin/', RedirectView.as_view(url='/accounts/', permanent=True)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

_ADDITIONAL_MODULES = ('help',)


for additional_module in _ADDITIONAL_MODULES:
    module_url = f'{additional_module}/'
    urls_path = f'{additional_module}.urls'
    urlpatterns.append(path(module_url, include((urls_path, additional_module))))
