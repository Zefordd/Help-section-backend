from django.utils.decorators import method_decorator
from help import models as help_models
from help import serializers as help_serializers
from help.constants import BASE_PAGE_URL
from help.schema_decorators import instructions_schema
from mainapp.utils import get_user_roles
from rest_framework import mixins, viewsets


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
