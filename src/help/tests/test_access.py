import pytest
from conftest import auth_client, get_groups_statuses_map
from django.conf import settings
from mainapp.auth import GroupName
from rest_framework import status
from rest_framework.reverse import reverse


class TestMediaAccess:
    @pytest.mark.parametrize('file_type, file_path', [('image', settings.TEST_IMAGE), ('document', settings.TEST_PDF)])
    @pytest.mark.parametrize(
        'group, status_code',
        get_groups_statuses_map(
            {GroupName.admin: status.HTTP_201_CREATED, GroupName.content_manager: status.HTTP_201_CREATED}
        ),
    )
    def test_create_image(self, client, group, file_type, file_path, status_code):
        client = auth_client(client, group)
        url = reverse(f'help:help_media-{file_type}')
        self._test_file(client, url, status_code, file_path)

    def _test_file(self, client, url, status_code, file_path):
        with open(file_path, 'rb') as import_file:
            upload_import_file = client.post(url, data={'file': import_file})
            assert upload_import_file.status_code == status_code
