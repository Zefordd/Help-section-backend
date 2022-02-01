from attachment.views import MediaViewSet
from help import custom_permissions
from help import models as help_models
from help import serializers as help_serializers
from rest_framework import mixins, viewsets
from rest_framework.decorators import action


class HelpMediaViewSet(MediaViewSet):
    permission_classes = (custom_permissions.HelpPermission,)
    _document_serializer = help_serializers.HelpDocumentSerializer

    @action(detail=False, methods=['POST'])
    def document(self, request):
        return self.upload_documents_api_method(request)

    @action(detail=False, methods=['POST'])
    def image(self, request):
        return self.upload_images_api_method(request)


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
