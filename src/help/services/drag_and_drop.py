from functools import lru_cache
from typing import Dict, Union

from help.models import ArticleContent, Section, Subsection
from rest_framework.exceptions import ValidationError


class BaseUpdateObjectOrderService:
    model = NotImplemented

    def update_objects_order(self, objects_order_data: dict):
        self._validate_request_data(tuple(objects_order_data.keys()))
        self._update_objects_order(objects_order_data)

    def _validate_request_data(self, object_ids: tuple):
        objects_map = self._get_objects_map(object_ids)
        if len(objects_map) == len(object_ids):
            return
        non_existent_object_ids = set(object_ids) - set(objects_map.keys())
        raise ValidationError(f'There is no {self.model.__name__} instances with ids: {non_existent_object_ids}')

    def _update_objects_order(self, objects_order_data: dict):
        objects_map = self._get_objects_map(tuple(objects_order_data.keys()))
        to_update = []
        for object_id, order in objects_order_data.items():
            obj = objects_map[int(object_id)]
            obj.order = order
            to_update.append(obj)
        self.model.objects.bulk_update(to_update, fields=('order',))

    @lru_cache
    def _get_objects_map(self, ids: tuple) -> Dict[int, Union[Section, Subsection, ArticleContent]]:
        objects = self.model.objects.filter(id__in=ids).all()
        return {int(obj.pk): obj for obj in objects}


class SectionsOrderUpdateService(BaseUpdateObjectOrderService):
    model = Section


class SubsectionsOrderUpdateService(BaseUpdateObjectOrderService):
    model = Subsection


class ArticleContentOrderUpdateService(BaseUpdateObjectOrderService):
    model = ArticleContent
