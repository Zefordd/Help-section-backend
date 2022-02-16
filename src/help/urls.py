from rest_framework import routers

from . import views

urlpatterns = []


router = routers.SimpleRouter()

router.register('media', views.HelpMediaViewSet, basename='help_media')

router.register('section', views.SectionViewSet, basename='section')
router.register('subsection', views.SubsectionViewSet, basename='subsection')
router.register('article_content', views.ArticleContentViewSet, basename='article_content')

router.register('instructions/section', views.SectionInstructionsViewSet, basename='section_instruction')
router.register('instructions/subsection', views.SubsectionInstructionsViewSet, basename='subsection_instruction')

router.register('role', views.HelpRoleViewSet, basename='role')

urlpatterns.extend(router.urls)
