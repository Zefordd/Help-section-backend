from conftest import auth_client
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


class TestInstructions:
    def test_instructions(self, client, instructions):
        client = auth_client(client, 'customer')
        section, subsection = instructions

        section_response = client.get(reverse('help:section_instruction-list'))
        assert section_response.status_code == HTTP_200_OK
        data = section_response.data
        self._test_section(data, section, subsection)

        subsection_response = client.get(reverse('help:subsection_instruction-detail', kwargs={'pk': subsection.pk}))
        assert subsection_response.status_code == HTTP_200_OK
        subsection_data = subsection_response.data
        self._test_subsection(subsection_data, subsection)
        assert len(subsection_data['article_content']) == 2
        assert 'subtitle' in subsection_data['article_content'][0]
        assert subsection_data['article_content'][0]['subtitle'] == 'subtitle'
        assert subsection_data['article_content'][1]['text'] == 'text'

    def test_instructions_with_page_url(self, client, instructions, instructions_with_page_url):
        client = auth_client(client, 'content_manager')
        section, subsection = instructions_with_page_url

        section_data = client.get(reverse('help:section_instruction-list'), data={'page_url': '/test_url/'}).data
        self._test_section(section_data, section, subsection)

        subsection_data = client.get(reverse('help:subsection_instruction-detail', kwargs={'pk': subsection.pk})).data
        self._test_subsection(subsection_data, subsection)

    def test_instructions_roles(self, client, instructions_with_roles):
        client = auth_client(client, 'customer')
        section, customer_subsection, manager_subsection = instructions_with_roles

        customer_data = client.get(reverse('help:section_instruction-list'), data={'page_url': '/test_url/'}).data
        assert len(customer_data) == 1
        self._test_section(customer_data, section, customer_subsection)

        client = auth_client(client, 'manager')
        manager_data = client.get(reverse('help:section_instruction-list'), data={'page_url': '/test_url/'}).data
        assert len(manager_data) == 1
        self._test_section(manager_data, section, manager_subsection)

    def test_instructions_wo_roles(self, client, instructions_wo_roles):
        client = auth_client(client, 'customer')
        _, subsection = instructions_wo_roles

        section_data = client.get(reverse('help:section_instruction-list')).data
        assert len(section_data) == 0

        subsection_response = client.get(reverse('help:subsection_instruction-detail', kwargs={'pk': subsection.pk}))
        assert subsection_response.status_code == HTTP_404_NOT_FOUND

    def test_instructions_status(self, client, unpublished_instructions):
        client = auth_client(client, 'customer')
        data = client.get(reverse('help:section_instruction-list')).data
        assert len(data) == 0

    def test_deleted_instruction(self, client, deleted_instructions):
        client = auth_client(client, 'customer')
        data = client.get(reverse('help:section_instruction-list')).data
        assert len(data) == 0

    def _test_section(self, data, section, subsection):
        assert len(data) == 1
        assert data[0]['id'] == section.id
        assert data[0]['name'] == section.name
        assert data[0]['status'] == section.status
        assert data[0]['page_url'] == section.page_url
        subsection_data = data[0]['subsections'][0]
        assert subsection_data['id'] == subsection.pk
        assert subsection_data['name'] == subsection.name
        assert subsection_data['order'] == subsection.order

    def _test_subsection(self, data, subsection):
        assert data['id'] == subsection.pk
        assert data['section_id'] == subsection.section.pk
        assert data['status'] == subsection.status
        assert data['order'] == subsection.order
        assert 'roles' in data
        assert 'documents' in data
