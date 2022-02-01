from rest_framework import routers

from . import views

urlpatterns = []


router = routers.SimpleRouter()

router.register('media', views.HelpMediaViewSet, basename='help_media')

router.register('section', views.SectionViewSet, basename='section')
router.register('subsection', views.SubsectionViewSet, basename='subsection')

urlpatterns.extend(router.urls)
