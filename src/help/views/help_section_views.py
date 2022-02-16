"""
API endpoints for help section data management (admin panel)
"""


from help import custom_permissions
from help import models as help_models
from help import serializers as help_serializers
from help.services.help_information_crud import delete_section, delete_subsection
from rest_framework import mixins, viewsets


class SectionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = help_models.Section.objects.prefetch_related('subsections').filter(deleted_at__isnull=True).all()
    serializer_class = help_serializers.SectionSerializer
    permission_classes = (custom_permissions.HelpPermission,)

    def perform_destroy(self, instance):
        delete_section(instance, self.request.user)


class SubsectionViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        help_models.Subsection.objects.prefetch_related(
            'article_content', 'article_content__image', 'roles', 'documents'
        )
        .filter(deleted_at__isnull=True)
        .all()
    )
    serializer_class = help_serializers.SubsectionSerializer
    permission_classes = (custom_permissions.HelpPermission,)

    def perform_destroy(self, instance):
        delete_subsection(instance, self.request.user)


class ArticleContentViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = help_models.ArticleContent.objects.all()
    serializer_class = help_serializers.ArticleContentSerializer
    permission_classes = (custom_permissions.HelpPermission,)
