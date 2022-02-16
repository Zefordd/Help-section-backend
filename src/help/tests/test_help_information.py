from conftest import auth_client
from help.constants import ArticleContentType, ReferenceInfoStatus
from help.models import ArticleContent, Section, Subsection
from help.services.help_information_crud import remove_deleted_help_info_instances
from help.tests.conftest import get_article_content
from mainapp.models import User
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class TestSection:
    def test_unpublish_child_subsections(self, client, published_section_with_subsections):
        client = auth_client(client, 'content_manager')
        section, subsection_1, subsection_2 = published_section_with_subsections
        for instance in section, subsection_1, subsection_2:
            assert instance.status == ReferenceInfoStatus.published
        client.patch(
            reverse('help:section-detail', kwargs={'pk': section.pk}),
            data={'status': ReferenceInfoStatus.unpublished},
            format='json',
        )
        section = Section.objects.get(pk=section.pk)
        assert section.status == ReferenceInfoStatus.unpublished
        for instance in section.subsections.all():
            assert instance.status == ReferenceInfoStatus.unpublished

    def test_publish_section_wo_content(self, client, section_wo_content):
        client = auth_client(client, 'content_manager')
        response = client.patch(
            reverse('help:section-detail', kwargs={'pk': section_wo_content.pk}),
            data={'status': ReferenceInfoStatus.published},
            format='json',
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert 'subsection wo content' in response.data[0]

    def test_publish_section_with_empty_content(self, client, section_with_empty_content):
        client = auth_client(client, 'content_manager')
        response = client.patch(
            reverse('help:section-detail', kwargs={'pk': section_with_empty_content.pk}),
            data={'status': ReferenceInfoStatus.published},
            format='json',
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert 'subsection with empty content' in response.data[0]

    def test_publish_section_with_content(self, client, section_with_content):
        section, subsection = section_with_content
        assert section.status == ReferenceInfoStatus.unpublished
        assert subsection.status == ReferenceInfoStatus.unpublished
        client = auth_client(client, 'content_manager')
        response = client.patch(
            reverse('help:section-detail', kwargs={'pk': section.pk}),
            data={'status': ReferenceInfoStatus.published},
            format='json',
        )
        assert response.status_code == HTTP_200_OK
        section, subsection = Section.objects.get(pk=section.pk), Subsection.objects.get(pk=subsection.pk)
        assert section.status == ReferenceInfoStatus.published
        assert subsection.status == ReferenceInfoStatus.published

    def test_create_section(self, client):
        user = User.objects.get(username='content_manager')
        client.force_authenticate(user)
        response = client.post(reverse('help:section-list'), data={'name': 'test_create_section'})
        section = Section.objects.get(id=response.data['id'])
        assert section.created_by == user
        subsections = section.subsections.all()
        assert len(subsections) == 1
        assert subsections[0].name == 'New section'
        assert subsections[0].order == 1
        assert subsections[0].status == ReferenceInfoStatus.unpublished

    def test_updated_by(self, client, section_wo_content):
        section = section_wo_content
        assert section.updated_by is None
        user = User.objects.get(username='content_manager')
        client.force_authenticate(user)
        client.patch(
            reverse('help:section-detail', kwargs={'pk': section.pk}), data={'order': 2}, format='json',
        )
        section = Section.objects.get(pk=section.pk)
        assert section.updated_by == user

    def test_delete_section(self, client, published_section_with_subsections):
        section, subsection_1, subsection_2 = published_section_with_subsections
        user = User.objects.get(username='content_manager')
        client.force_authenticate(user)
        assert section.status == ReferenceInfoStatus.published
        assert section.deleted_at is None

        response = client.get(reverse('help:section-detail', kwargs={'pk': section.pk}))
        assert response.status_code == HTTP_200_OK
        response = client.get(reverse('help:subsection-detail', kwargs={'pk': subsection_1.pk}))
        assert response.status_code == HTTP_200_OK

        client.delete(reverse('help:section-detail', kwargs={'pk': section.pk}))

        response = client.get(reverse('help:section-detail', kwargs={'pk': section.pk}))
        assert response.status_code == HTTP_404_NOT_FOUND
        response = client.get(reverse('help:subsection-detail', kwargs={'pk': subsection_1.pk}))
        assert response.status_code == HTTP_404_NOT_FOUND

        section = Section.objects.get(pk=section.pk)
        assert section.status == ReferenceInfoStatus.unpublished
        assert section.deleted_at is not None
        assert section.updated_by == user

        subsection = Subsection.objects.get(pk=subsection_1.pk)
        assert subsection.status == ReferenceInfoStatus.unpublished
        assert subsection.deleted_at is not None
        assert subsection.updated_by == user


class TestSubsection:
    def test_create_subsection(self, client, section):
        user = User.objects.get(username='content_manager')
        client.force_authenticate(user)
        response = client.post(
            reverse('help:subsection-list'),
            data={'name': 'test_create_section', 'section_id': section.pk},
            format='json',
        )
        subsection = Subsection.objects.get(id=response.data['id'])
        assert subsection.created_by == user

    def test_unpublish_single_subsection(self, client, single_published_subsection):
        client = auth_client(client, 'content_manager')
        section, subsection = single_published_subsection
        for instance in section, subsection:
            assert instance.status == ReferenceInfoStatus.published
        client.patch(
            reverse('help:subsection-detail', kwargs={'pk': subsection.pk}),
            data={'status': ReferenceInfoStatus.unpublished},
            format='json',
        )
        section = Section.objects.get(pk=section.pk)
        subsection = Subsection.objects.get(pk=subsection.pk)
        assert section.status == ReferenceInfoStatus.unpublished
        assert subsection.status == ReferenceInfoStatus.unpublished

    def test_publish_subsection(self, client, subsection_with_content):
        section, subsection = subsection_with_content
        user = User.objects.get(username='content_manager')
        assert section.status == ReferenceInfoStatus.unpublished
        assert subsection.status == ReferenceInfoStatus.unpublished
        client.force_authenticate(user)
        client.patch(
            reverse('help:subsection-detail', kwargs={'pk': subsection.pk}),
            data={'status': ReferenceInfoStatus.published},
            format='json',
        )
        section, subsection = Section.objects.get(pk=section.pk), Subsection.objects.get(pk=subsection.pk)
        assert section.status == ReferenceInfoStatus.published
        assert subsection.status == ReferenceInfoStatus.published
        assert section.updated_by == user
        assert subsection.updated_by == user

    def test_publish_subsection_wo_content(self, client, subsection_wo_content):
        client = auth_client(client, 'content_manager')
        response = client.patch(
            reverse('help:subsection-detail', kwargs={'pk': subsection_wo_content.pk}),
            data={'status': ReferenceInfoStatus.published},
            format='json',
        )
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_publish_subsection_with_empty_content(self, client, subsection_with_empty_content):
        client = auth_client(client, 'content_manager')
        response = client.patch(
            reverse('help:subsection-detail', kwargs={'pk': subsection_with_empty_content.pk}),
            data={'status': ReferenceInfoStatus.published},
            format='json',
        )
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_delete_single_subsection(self, client, single_published_subsection):
        section, subsection = single_published_subsection
        user = User.objects.get(username='content_manager')
        client.force_authenticate(user)
        for instance in section, subsection:
            assert instance.status == ReferenceInfoStatus.published
            assert instance.deleted_at is None

        client.delete(reverse('help:subsection-detail', kwargs={'pk': subsection.pk}))
        response = client.get(reverse('help:section-detail', kwargs={'pk': section.pk}))
        assert response.status_code == HTTP_404_NOT_FOUND
        response = client.get(reverse('help:subsection-detail', kwargs={'pk': subsection.pk}))
        assert response.status_code == HTTP_404_NOT_FOUND
        section, subsection = Section.objects.get(pk=section.pk), Subsection.objects.get(pk=subsection.pk)
        for instance in section, subsection:
            assert instance.status == ReferenceInfoStatus.unpublished
            assert instance.deleted_at is not None
            assert instance.updated_by == user

    def test_delete_subsection(self, client, published_section_with_subsections):
        client = auth_client(client, 'content_manager')
        section, subsection, _ = published_section_with_subsections
        client.delete(reverse('help:subsection-detail', kwargs={'pk': subsection.pk}))
        response = client.get(reverse('help:section-detail', kwargs={'pk': section.pk}))
        assert response.status_code == HTTP_200_OK

        section, subsection = Section.objects.get(pk=section.pk), Subsection.objects.get(pk=subsection.pk)
        assert section.deleted_at is None
        assert subsection.deleted_at is not None


class TestArticleContent:
    def test_has_article_content(self):
        for content_type in ArticleContentType:
            content = get_article_content(content_type, content_type)
            assert content.has_content() is True

        for content_type in ArticleContentType:
            content = get_article_content(content_type, None)
            assert content.has_content() is False


class TestRemoveDeletedHelpInfo:
    def test_remove_deleted_section(self, deleted_section):
        self._test_count_models(1, 1, 1)
        remove_deleted_help_info_instances()
        self._test_count_models(0, 0, 0)

    def test_remove_subsection(self, deleted_subsection):
        self._test_count_models(1, 2, 2)
        remove_deleted_help_info_instances()
        self._test_count_models(1, 1, 1)

    def _test_count_models(self, sections_amount, subsections_amount, content_amount):
        assert Section.objects.count() == sections_amount
        assert Subsection.objects.count() == subsections_amount
        assert ArticleContent.objects.count() == content_amount
