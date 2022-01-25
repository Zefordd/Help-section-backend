from attachment.views import MediaViewSet
from help import custom_permissions
from help.serializers import HelpDocumentSerializer
from rest_framework.decorators import action


class HelpMediaViewSet(MediaViewSet):
    permission_classes = (custom_permissions.HelpPermission,)
    _document_serializer = HelpDocumentSerializer

    @action(detail=False, methods=['POST'])
    def document(self, request):
        return self.upload_documents_api_method(request)

    @action(detail=False, methods=['POST'])
    def image(self, request):
        return self.upload_images_api_method(request)
