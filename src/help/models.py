from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from help.constants import ReferenceInfoStatus


class LastActionModel(models.Model):
    created_by = models.ForeignKey(
        'mainapp.User', on_delete=models.SET_NULL, related_name='created_%(class)ss', null=True, blank=True
    )
    updated_by = models.ForeignKey(
        'mainapp.User', on_delete=models.SET_NULL, related_name='updated_%(class)ss', null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Section(LastActionModel):
    name = models.CharField(max_length=250)
    status = models.CharField(
        choices=ReferenceInfoStatus.choices, max_length=120, default=ReferenceInfoStatus.unpublished
    )
    page_url = models.CharField(max_length=250, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def get_max_order(self):
        return self._meta.model.objects.aggregate(max_num=models.Max('order'))['max_num']

    def is_released(self):
        return self.status == ReferenceInfoStatus.published

    class Meta:
        ordering = ('order', 'id')


class Subsection(LastActionModel):
    section = models.ForeignKey(Section, related_name='subsections', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    status = models.CharField(
        choices=ReferenceInfoStatus.choices, max_length=120, default=ReferenceInfoStatus.unpublished
    )
    roles = models.ManyToManyField(to=Group, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def get_max_order(self):
        return self._meta.model.objects.filter(section=self.section).aggregate(max_num=models.Max('order'))['max_num']

    def is_released(self):
        return self.status == ReferenceInfoStatus.published

    class Meta:
        ordering = ('order', 'id')
