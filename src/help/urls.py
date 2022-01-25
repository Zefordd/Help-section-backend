from rest_framework import routers

from . import views

urlpatterns = []


router = routers.SimpleRouter()

router.register('media', views.HelpMediaViewSet, basename='help_media')

urlpatterns.extend(router.urls)
