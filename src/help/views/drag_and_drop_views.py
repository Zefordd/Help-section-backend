from help import models as help_models
from help.custom_permissions import HelpPermission
from help.schema_decorators import drag_and_drop_schema
from help.services.drag_and_drop import (
    ArticleContentOrderUpdateService,
    SectionsOrderUpdateService,
    SubsectionsOrderUpdateService,
)
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseOrderUpdateView(APIView):
    service_class = NotImplemented
    queryset = NotImplemented
    permission_classes = (HelpPermission,)

    @drag_and_drop_schema()
    def put(self, request, *args, **kwargs):
        self.service_class().update_objects_order(request.data)
        return Response()


class SectionOrderUpdateView(BaseOrderUpdateView):
    service_class = SectionsOrderUpdateService
    queryset = help_models.Section.objects.filter(deleted_at__isnull=True)


class SubsectionOrderUpdateView(BaseOrderUpdateView):
    service_class = SubsectionsOrderUpdateService
    queryset = help_models.Subsection.objects.filter(deleted_at__isnull=True)


class ArticleContentOrderUpdateView(BaseOrderUpdateView):
    service_class = ArticleContentOrderUpdateService
    queryset = help_models.ArticleContent.objects.all()
