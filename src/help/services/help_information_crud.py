from typing import Union

from help.constants import ReferenceInfoStatus
from help.models import Section, Subsection
from mainapp.models import User
from rest_framework.serializers import ValidationError


def unpublish_child_subsections(section: Section, user: User):
    section.subsections.update(status=ReferenceInfoStatus.unpublished, updated_by=user)


def publish_child_subsections(section: Section, user: User):
    section.subsections.update(status=ReferenceInfoStatus.published, updated_by=user)


def subsection_has_content(subsection: Subsection) -> bool:
    articles_content = subsection.article_content.all()
    if not articles_content:
        return False
    for content in articles_content:
        if content.has_content():
            return True
    return False


def get_unpublished_child_subsections_wo_content(section: Section) -> set[Subsection]:
    subsections_wo_content = set()
    subsections = (
        section.subsections.filter(status=ReferenceInfoStatus.unpublished, deleted_at__isnull=True)
        .prefetch_related('article_content')
        .all()
    )
    for subsection in subsections:
        if not subsection_has_content(subsection):
            subsections_wo_content.add(subsection)
    return subsections_wo_content


def is_published_instance(new_status: str, instance: Union[Section, Subsection]) -> bool:
    already_published = not new_status and instance.status == ReferenceInfoStatus.published
    will_be_published = new_status == ReferenceInfoStatus.published
    return already_published or will_be_published


def update_section(section: Section, user: User, data: dict):
    if section.is_released and data.get('status') == ReferenceInfoStatus.unpublished:
        unpublish_child_subsections(section, user)
    if is_published_instance(data.get('status'), section):
        subsections_wo_content = get_unpublished_child_subsections_wo_content(section)
        if subsections_wo_content:
            subs_names = [subs.name for subs in subsections_wo_content]
            err_msg = 'Add content to subsections (' + '; '.join(subs_names) + ';)'
            raise ValidationError(err_msg)
        publish_child_subsections(section, user)
