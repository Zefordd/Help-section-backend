from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('sections_order/', views.SectionOrderUpdateView.as_view(), name='sections_order'),
    path('subsections_order/', views.SubsectionOrderUpdateView.as_view(), name='subsections_order'),
    path('article_content_order/', views.ArticleContentOrderUpdateView.as_view(), name='article_content_order'),
]


router = routers.SimpleRouter()

router.register('media', views.HelpMediaViewSet, basename='help_media')
router.register('role', views.HelpRoleViewSet, basename='role')

router.register('section', views.SectionViewSet, basename='section')
router.register('subsection', views.SubsectionViewSet, basename='subsection')
router.register('article_content', views.ArticleContentViewSet, basename='article_content')

router.register('instructions/section', views.SectionInstructionsViewSet, basename='section_instruction')
router.register('instructions/subsection', views.SubsectionInstructionsViewSet, basename='subsection_instruction')


urlpatterns.extend(router.urls)
