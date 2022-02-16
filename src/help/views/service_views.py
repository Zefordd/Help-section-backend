"""
API endpoints for fields with select options and media content
"""


from attachment.views import MediaViewSet
from django.contrib.auth.models import Group
from help import custom_permissions
from help import serializers as help_serializers
from rest_framework import viewsets
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


class HelpRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().select_related('group_property').order_by('id')
    serializer_class = help_serializers.RoleSerializer
    permission_classes = (custom_permissions.HelpPermission,)
    pagination_class = None
