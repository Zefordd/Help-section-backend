from datetime import datetime, timedelta

import pytest
from conftest import get_test_file_attachment
from django.contrib.auth.models import Group
from help.constants import ArticleContentType, ReferenceInfoStatus
from help.models import ArticleContent, Section, Subsection
from mainapp.auth import GroupName


@pytest.fixture
def published_section_with_subsections():
    section = Section.objects.create(name='test_section', status=ReferenceInfoStatus.published)
    subsection_1 = Subsection.objects.create(section=section, name='subs 1', status=ReferenceInfoStatus.published)
    subsection_2 = Subsection.objects.create(section=section, name='subs 2', status=ReferenceInfoStatus.published)
    return section, subsection_1, subsection_2


def get_article_content(content_type, content=None):
    section = Section.objects.create(name='_test_section', status=ReferenceInfoStatus.published)
    subsection = Subsection.objects.create(section=section, name='_test_subs', status=ReferenceInfoStatus.published)
    article_content = ArticleContent.objects.create(subsection=subsection, content_type=content_type)
    if content is None:
        return article_content
    if content_type == ArticleContentType.image:
        image = get_test_file_attachment(content)
        content = image
    setattr(article_content, content_type, content)
    article_content.save()
    return article_content


@pytest.fixture
def section_wo_content():
    section = Section.objects.create(name='test_section', status=ReferenceInfoStatus.unpublished)
    Subsection.objects.create(section=section, name='subsection wo content', status=ReferenceInfoStatus.unpublished)
    return section


@pytest.fixture
def section_with_empty_content():
    section = Section.objects.create(name='test_section with empty content', status=ReferenceInfoStatus.unpublished)
    subsection = Subsection.objects.create(
        section=section, name='subsection with empty content', status=ReferenceInfoStatus.unpublished
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text)
    return section


@pytest.fixture
def section_with_content():
    section = Section.objects.create(name='test_section with content', status=ReferenceInfoStatus.unpublished)
    subsection = Subsection.objects.create(
        section=section, name='subsection with content', status=ReferenceInfoStatus.unpublished
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, text='test text')
    return section, subsection


@pytest.fixture
def section():
    return Section.objects.create(name='single section', status=ReferenceInfoStatus.unpublished)


@pytest.fixture
def single_published_subsection():
    section = Section.objects.create(name='test_section', status=ReferenceInfoStatus.published)
    subsection = Subsection.objects.create(section=section, name='subs 1', status=ReferenceInfoStatus.published)
    return section, subsection


@pytest.fixture
def subsection_with_content():
    section = Section.objects.create(name='test subs with content', status=ReferenceInfoStatus.unpublished)
    subsection = Subsection.objects.create(
        section=section, name='subsection with content', status=ReferenceInfoStatus.unpublished
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, text='test text')
    return section, subsection


@pytest.fixture
def subsection_wo_content():
    section = Section.objects.create(name='test_subsection section', status=ReferenceInfoStatus.unpublished)
    subsection = Subsection.objects.create(
        section=section, name='subsection wo content', status=ReferenceInfoStatus.unpublished
    )
    return subsection


@pytest.fixture
def subsection_with_empty_content():
    section = Section.objects.create(name='test_subsection with empty content', status=ReferenceInfoStatus.unpublished)
    subsection = Subsection.objects.create(
        section=section, name='subsection with empty content', status=ReferenceInfoStatus.unpublished
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text)
    return subsection


@pytest.fixture
def instructions():
    section = Section.objects.create(name='section wo page_url', status=ReferenceInfoStatus.published)
    subsection = Subsection.objects.create(section=section, name='subsection', status=ReferenceInfoStatus.published)
    all_roles = Group.objects.all()
    subsection.roles.add(*all_roles)
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, text='text', order=2)
    ArticleContent.objects.create(
        subsection=subsection, content_type=ArticleContentType.subtitle, subtitle='subtitle', order=1
    )
    return section, subsection


@pytest.fixture
def instructions_with_page_url():
    section = Section.objects.create(
        name='section with page_url', status=ReferenceInfoStatus.published, page_url='/test_url/'
    )
    subsection = Subsection.objects.create(
        section=section, name='subsection with page_url', status=ReferenceInfoStatus.published
    )
    all_roles = Group.objects.all()
    subsection.roles.add(*all_roles)
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, text='text page url')
    return section, subsection


@pytest.fixture
def instructions_with_roles():
    section = Section.objects.create(
        name='section with roles', status=ReferenceInfoStatus.published, page_url='/test_url/'
    )
    customer_role = Group.objects.filter(name=GroupName.customer).first()

    customer_subsection = Subsection.objects.create(
        section=section, name='customer subsection', status=ReferenceInfoStatus.published
    )
    customer_subsection.roles.add(customer_role)
    ArticleContent.objects.create(
        subsection=customer_subsection, content_type=ArticleContentType.text, text='customer text'
    )

    manager_role = Group.objects.filter(name=GroupName.manager).first()
    manager_subsection = Subsection.objects.create(
        section=section, name='manager subsection', status=ReferenceInfoStatus.published
    )
    manager_subsection.roles.add(manager_role)
    ArticleContent.objects.create(
        subsection=manager_subsection, content_type=ArticleContentType.text, text='manager text'
    )
    return section, customer_subsection, manager_subsection


@pytest.fixture
def instructions_wo_roles():
    section = Section.objects.create(name='section', status=ReferenceInfoStatus.published)
    subsection = Subsection.objects.create(
        section=section, name='subsection wo roles', status=ReferenceInfoStatus.published
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, text='text', order=2)
    ArticleContent.objects.create(
        subsection=subsection, content_type=ArticleContentType.subtitle, subtitle='subtitle', order=1
    )
    return section, subsection


@pytest.fixture
def unpublished_instructions():
    section = Section.objects.create(name='published section', status=ReferenceInfoStatus.published)
    subsection = Subsection.objects.create(
        section=section, name='unpublished subsection', status=ReferenceInfoStatus.unpublished
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, subtitle='text')


@pytest.fixture
def deleted_instructions():
    section = Section.objects.create(name='section', status=ReferenceInfoStatus.unpublished)
    subsection = Subsection.objects.create(
        section=section, name='deleted subsection', status=ReferenceInfoStatus.unpublished, deleted_at=datetime.now()
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, subtitle='text')


@pytest.fixture
def deleted_section():
    nine_days_ago = datetime.now() - timedelta(days=9)
    section = Section.objects.create(name='section', status=ReferenceInfoStatus.unpublished, deleted_at=nine_days_ago)
    subsection = Subsection.objects.create(
        section=section, name='deleted subsection', status=ReferenceInfoStatus.unpublished, deleted_at=nine_days_ago
    )
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, subtitle='text')


@pytest.fixture
def deleted_subsection():
    nine_days_ago = datetime.now() - timedelta(days=9)
    section = Section.objects.create(name='section', status=ReferenceInfoStatus.published)
    deleted_subs = Subsection.objects.create(
        section=section, name='deleted subsection', status=ReferenceInfoStatus.unpublished, deleted_at=nine_days_ago
    )
    ArticleContent.objects.create(subsection=deleted_subs, content_type=ArticleContentType.text, subtitle='text')

    subsection = Subsection.objects.create(section=section, name='subsection', status=ReferenceInfoStatus.published)
    ArticleContent.objects.create(subsection=subsection, content_type=ArticleContentType.text, subtitle='text')


@pytest.fixture
def sections_order():
    section_1 = Section.objects.create(name='test_section_1', order=1)
    section_2 = Section.objects.create(name='test_section_2', order=2)
    section_3 = Section.objects.create(name='test_section_3', order=3)
    return section_1, section_2, section_3


@pytest.fixture
def subsections_order():
    section = Section.objects.create(name='section')
    subsection_1 = Subsection.objects.create(section=section, name='subsection_1', order=1)
    subsection_2 = Subsection.objects.create(section=section, name='subsection_2', order=2)
    subsection_3 = Subsection.objects.create(section=section, name='subsection_3', order=3)
    return subsection_1, subsection_2, subsection_3


@pytest.fixture
def article_order_order():
    section = Section.objects.create(name='section')
    subsection = Subsection.objects.create(section=section, name='subsection')
    content_1 = ArticleContent.objects.create(subsection=subsection, text='foo_1', order=1)
    content_2 = ArticleContent.objects.create(subsection=subsection, text='foo_2', order=2)
    content_3 = ArticleContent.objects.create(subsection=subsection, text='foo_3', order=3)
    return content_1, content_2, content_3
