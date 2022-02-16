from attachment.views import MediaViewSet
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from help import custom_permissions
from help import models as help_models
from help import serializers as help_serializers
from help.constants import BASE_PAGE_URL
from help.schema_decorators import instructions_schema
from help.services.help_information_crud import delete_section, delete_subsection
from mainapp.utils import get_user_roles
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


class HelpRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().select_related('group_property').order_by('id')
    serializer_class = help_serializers.RoleSerializer
    permission_classes = (custom_permissions.HelpPermission,)
    pagination_class = None


@method_decorator(name='list', decorator=(instructions_schema()))
class SectionInstructionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = help_models.Section.objects.active()
    serializer_class = help_serializers.InstructionsSectionSerializer
    pagination_class = None

    def get_queryset(self):
        roles = get_user_roles(self.request.user)
        page_url = self.request.query_params.get('page_url', BASE_PAGE_URL)
        return help_models.Section.objects.instructions(roles=roles, page_url=page_url)


class SubsectionInstructionsViewSet(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet,
):
    queryset = help_models.Subsection.objects.all()
    serializer_class = help_serializers.SubsectionSerializer
    pagination_class = None

    def get_queryset(self):
        roles = get_user_roles(self.request.user)
        return help_models.Subsection.objects.content(roles=roles)
