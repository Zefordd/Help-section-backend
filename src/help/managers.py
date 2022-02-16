from typing import Sequence

from django.db import models
from django.db.models import Prefetch, Q
from help.constants import BASE_PAGE_URL, ReferenceInfoStatus


class SectionManager(models.Manager):
    def active(self) -> models.QuerySet:
        return self.get_queryset().filter(deleted_at__isnull=True, status=ReferenceInfoStatus.published)

    def instructions(self, roles: Sequence[str], page_url: str) -> models.QuerySet:
        """
        Prefetch all data for instructions
        """
        from help.models import Subsection  # avoid circular import

        sections_qs = (
            self.active()
            .filter(subsections__deleted_at__isnull=True, subsections__status=ReferenceInfoStatus.published)
            .filter(subsections__roles__name__in=roles)
        )
        if page_url != BASE_PAGE_URL:
            sections_qs = sections_qs.filter(Q(page_url=page_url) | Q(page_url=page_url + '/'))

        subsections_with_roles = Prefetch(
            lookup='subsections', to_attr='subsections_with_roles', queryset=Subsection.objects.with_roles(roles),
        )
        return sections_qs.prefetch_related(subsections_with_roles).distinct()


class SubsectionManager(models.Manager):
    def active(self) -> models.QuerySet:
        return self.get_queryset().filter(deleted_at__isnull=True, status=ReferenceInfoStatus.published).distinct()

    def with_roles(self, roles) -> models.QuerySet:
        """
        Return all active subsections with role filter
        """
        return self.active().filter(roles__name__in=roles)

    def content(self, roles) -> models.QuerySet:
        """
        Prefetch all subsection content
        """
        return self.with_roles(roles).prefetch_related(
            'article_content', 'article_content__image', 'roles', 'documents'
        )
