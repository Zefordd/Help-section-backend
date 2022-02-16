from datetime import datetime, timedelta
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


def is_single_subsection(subsection: Subsection) -> bool:
    return subsection.section.subsections.count() == 1


def unpublish_parent_section(subsection: Subsection, user: User):
    subsection.section.status = ReferenceInfoStatus.unpublished
    subsection.section.user = user
    subsection.section.save()


def publish_parent_section(subsection: Subsection, user: User):
    if subsection.section.status == ReferenceInfoStatus.published:
        return
    subsection.section.status = ReferenceInfoStatus.published
    subsection.section.updated_by = user
    subsection.section.save()


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


def update_subsection(subsection: Subsection, user: User, data: dict):
    if (
        subsection.is_released
        and data.get('status') == ReferenceInfoStatus.unpublished
        and is_single_subsection(subsection)
    ):
        unpublish_parent_section(subsection, user)
    if is_published_instance(data.get('status'), subsection):
        if not subsection_has_content(subsection):
            raise ValidationError('You need to add content to the subsection')
        publish_parent_section(subsection, user)


def delete_section(section: Section, user: User):
    now = datetime.now()
    section.status = ReferenceInfoStatus.unpublished
    section.deleted_at = now
    section.updated_by = user
    section.save()
    section.subsections.update(status=ReferenceInfoStatus.unpublished, deleted_at=now, updated_by=user)


def delete_subsection(subsection: Subsection, user: User):
    now = datetime.now()
    if is_single_subsection(subsection):
        return delete_section(subsection.section, user)
    subsection.status = ReferenceInfoStatus.unpublished
    subsection.deleted_at = now
    subsection.updated_by = user
    subsection.save()


def remove_deleted_help_info_instances():
    seven_days_ago = datetime.now() - timedelta(days=7)
    Section.objects.filter(deleted_at__lte=seven_days_ago).delete()
    Subsection.objects.filter(deleted_at__lte=seven_days_ago).delete()
