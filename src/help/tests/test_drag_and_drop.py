import pytest
from conftest import auth_client
from help.models import ArticleContent, Section, Subsection
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class TestDragAndDrop:
    def _test_update_objects_order(self, client, instances, model, url):
        client = auth_client(client, 'content_manager')
        instance_1, instance_2, instance_3 = instances
        for order, instance in enumerate((instance_1, instance_2, instance_3), 1):
            assert instance.order == order

        response = client.put(
            reverse(f'help:{url}'), data={instance_1.pk: 3, instance_2.pk: 1, instance_3.pk: 2}, format='json'
        )
        assert response.status_code == HTTP_200_OK

        instance_1, instance_2, instance_3 = (
            model.objects.filter(id__in=[instance_1.pk, instance_2.pk, instance_3.pk]).order_by('id').all()
        )
        assert instance_1.order == 3
        assert instance_2.order == 1
        assert instance_3.order == 2

    def test_update_sections_order(self, client, sections_order):
        self._test_update_objects_order(client, sections_order, Section, 'sections_order')

    def test_update_subsections_order(self, client, subsections_order):
        self._test_update_objects_order(client, subsections_order, Subsection, 'subsections_order')

    def test_update_article_content_order(self, client, article_order_order):
        self._test_update_objects_order(client, article_order_order, ArticleContent, 'article_content_order')

    @pytest.mark.parametrize('url', ('sections_order', 'subsections_order', 'article_content_order'))
    def test_validation(self, client, url):
        client = auth_client(client, 'content_manager')
        non_existent_id = 0
        response = client.put(reverse(f'help:{url}'), data={non_existent_id: 42}, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
