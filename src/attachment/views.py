from attachment.models import FileAttachment
from attachment.serializers import DocumentsSerializer, FileAttachmentSerializer, ImagesSerializer
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class MediaViewSet(viewsets.GenericViewSet):
    """
    Base view class for upload documents and images
    """

    serializer_class = FileAttachmentSerializer
    queryset = FileAttachment.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    _document_serializer = DocumentsSerializer
    _image_serializer = ImagesSerializer

    def upload_documents_api_method(self, request):
        file_attachment = self._upload_documents(request.data)
        return Response(self.get_serializer(file_attachment).data, status=status.HTTP_201_CREATED)

    def upload_images_api_method(self, request):
        file_attachment = self._upload_images(request.data)
        return Response(self.get_serializer(file_attachment).data, status=status.HTTP_201_CREATED)

    def _upload_documents(self, files):
        return self._upload_files(files, self._document_serializer)

    def _upload_images(self, files):
        return self._upload_files(files, self._image_serializer)

    def _upload_files(self, data, serializer_class):
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        file_attachment = FileAttachment.objects.create(name=data['file'].name, file=data['file'])
        return file_attachment
